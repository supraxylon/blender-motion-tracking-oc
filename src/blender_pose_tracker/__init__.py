# This file is part of the Blender Pose Tracker add-on.
# Install: copy this folder into Blender's scripts/addons/ directory,
#          then enable via Edit > Preferences > Add-ons.
#
# Target: Blender 4.2+
# Headless test (Windows):
#   "C:\Program Files\Blender Foundation\Blender 4.2\4.2\blender.exe" ^
#     --background --python <script>
#
# NOTE: bpy is only available when running inside Blender.
# py_compile works on this file because it contains no runtime bpy calls
# at module-level (only inside classes/functions registered inside Blender).
# blender_pose_tracker/importer.py has zero bpy imports and is always importable.

bl_info = {
    "name": "Pose Tracker",
    "author": "supraxylon",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Pose Tracker",
    "description": "Import cached MMPose pose JSON and create tracked empties.",
    "category": "Animation",
}

import contextlib
import os

with contextlib.suppress(ImportError):
    import bpy


def _register_bpy():
    """Register all classes and properties. Must be called from within Blender."""
    from .importer import KEYPOINT_NAMES

    # --- Operator class ---
    class OBJECT_OT_import_poses:
        bl_idname = "object.import_poses"
        bl_label = "Import Pose Tracks"
        bl_options = {"REGISTER", "UNDO"}

        filepath: bpy.props.StringProperty(
            subtype="FILE_PATH",
            description="Path to the cached MMPose tracking JSON file",
        )

        def execute(self, context):
            if not self.filepath:
                fp = context.scene.pose_tracker_input_path
                if fp:
                    self.filepath = fp
                if not self.filepath:
                    self.report({"ERROR"}, "No file path given")
                    return {"CANCELLED"}

            frame_start = context.scene.frame_start

            from .importer import import_poses
            data = import_poses(self.filepath)
            num_frames = len(data["frames"])

            # -- clear previous empties --
            for obj in list(bpy.data.objects):
                if obj.name.startswith("PoseTrack_"):
                    bpy.data.objects.remove(obj, do_unlink=True)

            empties = {}

            for frame in data["frames"]:
                scene_frame = frame_start + frame["frame_index"]
                for person in frame["persons"]:
                    track_id = person["track_id"]
                    person_name = (
                        str(track_id)
                        if track_id is not None
                        else "unknown"
                    )
                    for kp_idx, kp in enumerate(person["keypoints"]):
                        kp_name = (
                            KEYPOINT_NAMES[kp_idx]
                            if kp_idx < len(KEYPOINT_NAMES)
                            else f"kp_{kp_idx}"
                        )
                        obj_name = f"PoseTrack_{person_name}_{kp_name}"

                        if obj_name not in empties:
                            bpy.ops.object.empty_add(
                                type="SPHERE",
                                align="WORLD",
                                location=(0, 0, 0),
                                scale=(1, 1, 1),
                            )
                            empty = bpy.context.active_object
                            empty.name = obj_name
                            empty.empty_display_size = 0.15
                            empty["track_id"] = track_id
                            empty["kp_name"] = kp_name
                            empties[obj_name] = empty

                        # Normalized 0..1 -> simple Blender coords via offset
                        x = (kp["x"] - 0.5) * 10.0
                        y = -(kp["y"] - 0.5) * 10.0

                        empty.location = (x, y, 0.0)
                        empty.keyframe_insert(
                            data_path="location", frame=scene_frame
                        )

            self.report(
                {"INFO"},
                f"Imported {num_frames} frames from {os.path.basename(self.filepath)}",
            )
            return {"FINISHED"}

    # Panel class
    class VIEW3D_MT_pose_tracker_panel(bpy.types.Panel):
        bl_label = "Pose Tracker"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "Pose Tracker"

        def draw(self, context):
            layout = self.layout
            col = layout.column()
            col.label(text="Import cached pose JSON:")
            col.prop(context.scene, "pose_tracker_input_path", text="")
            op = col.operator("object.import_poses")
            fp = context.scene.pose_tracker_input_path
            if fp:
                op.filepath = fp

    # Property group
    class ScenePoseTrackerProps(bpy.types.PropertyGroup):
        input_path: bpy.props.StringProperty(
            default="",
            description="Path to the cached MMPose tracking JSON file",
        )

    # Register
    bpy.utils.register_class(OBJECT_OT_import_poses)
    bpy.utils.register_class(VIEW3D_MT_pose_tracker_panel)
    bpy.utils.register_class(ScenePoseTrackerProps)
    bpy.types.Scene.pose_tracker_input_path = bpy.props.StringProperty(
        default="",
        description="Path to the cached MMPose tracking JSON file",
    )

    return OBJECT_OT_import_poses, VIEW3D_MT_pose_tracker_panel, ScenePoseTrackerProps


def _unregister_bpy(cls_objects):
    """Unregister classes. Must be called from within Blender."""
    if cls_objects:
        bpy.utils.unregister_class(cls_objects[0])
        bpy.utils.unregister_class(cls_objects[1])
        bpy.utils.unregister_class(cls_objects[2])
    del bpy.types.Scene.pose_tracker_input_path


classes = None
_cls_objects = None


def register():
    global classes, _cls_objects
    _cls_objects = _register_bpy()
    classes = _cls_objects


def unregister():
    global _cls_objects
    if _cls_objects:
        _unregister_bpy(_cls_objects)
        _cls_objects = None


if __name__ == "__main__":
    register()
