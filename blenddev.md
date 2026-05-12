# Blender Motion Tracking - Development Guide

**Scope:** How to build, integrate, and deliver the MMPose-based motion tracking add-on for Blender.
**Target:** Blender 4.2+ (Python 3.11+), Windows/Linux/macOS.

---

## 1. THE EASIEST ROUTE: PURE PYTHON ADD-ON

Don't compile C++. Don't use Pybind11. The simplest, most maintainable path is:

```
Blend file (or install directory)
-- addons/
   -- motion_tracking/          -- Pure Python add-on
      -- __init__.py            -- Blender add-on entry point
      -- panel.py               -- UI panel in Video Editor
      -- operators.py           -- Run inference, import results
      -- retarget.py            -- Armature mapping presets
      -- config.py              -- MMPose paths, model selection
      `-- deps/
         `-- mmpose_worker/     -- Standalone Python script (your MMPose pipeline)
            -- __init__.py
            -- runner.py        -- MMPose inference loop
            `-- requirements.txt
```

### Why Pure Python?

1. **Blender already embeds Python.** You get bpy, bmesh, mathutils, json, pathlib - no external build toolchain.
2. **No C++ toolchain setup.** Pybind11 requires TorchScript/ONNX C++ toolchain, nvcc, Blender SDK includes. Pure Python avoids all of that.
3. **Instant iteration.** Edit -> Save -> Reload in Blender. C++ requires compile -> copy -> reload.
4. **MMPose is Python-native.** MMPose runs in Python. Wrapping C++ around Python-wrapped C++ is pointless.
5. **Out-of-process is already mandated.** MMPose worker runs as a separate Python subprocess. The add-on just:
   - Loads video in Video Editor
   - Launches subprocess.run(["python", "deps/mmpose_worker/runner.py", ...])
   - Reads JSON output
   - Creates empties/bones/curves via bpy.ops.*

**Bottom line:** The add-on is a thin UI + data-mapping layer. MMPose does all heavy lifting as a subprocess.

---

## 2. BLENDER ADD-ON STRUCTURE

### 2.1 Entry Point (__init__.py)

```python
import bpy
from .panel import MotionTrackingPanel
from .operators import (
    MTC_OT_run_tracking,
    MTC_OT_import_keypoints,
    MTC_OT_create_armature,
    MTC_OT_clear_tracks,
)

bl_info = {
    "name": "Motion Tracking (MMPose)",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "Video Editor > Sidebar > Motion Tracking",
    "description": "Run MMPose on loaded video and retarget to armature.",
    "category": "Animation",
}

classes = (MotionTrackingPanel, MTC_OT_run_tracking, MTC_OT_import_keypoints,
           MTC_OT_create_armature, MTC_OT_clear_tracks)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

### 2.2 UI Panel (appears in Video Editor sidebar -> "Motion Tracking" tab)

```python
import bpy

class MotionTrackingPanel(bpy.types.Panel):
    bl_label = "Motion Tracking"
    bl_idname = "MTC_PT_panel"
    bl_space_type = 'SEQUENCE_EDITOR'  # Video Edit workspace uses Sequencer
    bl_region_type = 'UI'
    bl_category = "Motion Tracking"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Video input
        layout.prop(scene, "mtc_movie_file")
        
        # MMPose model config
        layout.prop(scene, "mtc_pose_model")
        layout.prop(scene, "mtc_device")
        
        # Person selection
        layout.prop(scene, "mtc_person_id")
        layout.label(text=f"Detected: {scene.mtc_persons_detected} people")
        
        # Actions
        col = layout.column()
        col.operator("mtc.run_tracking", text="Run Inference")
        col.operator("mtc.import_keypoints", text="Import to Empties")
        col.operator("mtc.create_armature", text="Create Armature")
        
        layout.separator()
        layout.operator("mtc.clear_tracks", text="Clear All Tracks")
```

### 2.3 Key Operators

```python
import bpy
import subprocess
import json
import os
from mathutils import Vector

class MTC_OT_run_tracking(bpy.types.Operator):
    """Run MMPose inference on the loaded video"""
    bl_idname = "mtc.run_tracking"
    bl_label = "Run MMPose Inference"
    
    def execute(self, context):
        # 1. Get movie clip from current scene
        clip = context.scene.active_video_strip?.clip
        if not clip:
            self.report({'ERROR'}, "No movie clip loaded")
            return {'CANCELLED'}
        
        # 2. Launch MMPose worker subprocess
        worker_path = os.path.join(os.path.dirname(__file__), "deps/mmpose_worker/runner.py")
        result_path = bpy.path.abspath("//mtc_output.json")
        
        cmd = [
            "python", worker_path,
            "-i", clip.filepath,
            "-o", result_path,
            "-m", context.scene.mtc_pose_model,
            "-d", context.scene.mtc_device,
        ]
        
        self.report({'INFO'}, f"Running MMPose: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            self.report({'ERROR'}, f"MMPose error: {result.stderr}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, "MMPose complete")
        return {'FINISHED'}

class MTC_OT_import_keypoints(bpy.types.Operator):
    """Import JSON keypoints to Blender empties"""
    bl_idname = "mtc.import_keypoints"
    bl_label = "Import Keypoints"
    
    def execute(self, context):
        result_path = bpy.path.abspath("//mtc_output.json")
        with open(result_path) as f:
            data = json.load(f)
        
        self._create_empties_for_person(data, context.scene.mtc_person_id)
        return {'FINISHED'}
    
    def _create_empties_for_person(self, data, person_id):
        """Create/move empties for each detected keypoint"""
        keypoint_map = {
            'nose': 'Nose',
            'left_eye': 'LeftEye', 'right_eye': 'RightEye',
            'left_ear': 'LeftEar', 'right_ear': 'RightEar',
            'left_shoulder': 'LShoulder', 'right_shoulder': 'RShoulder',
            'left_elbow': 'LElbow', 'right_elbow': 'RElbow',
            'left_wrist': 'LWrist', 'right_wrist': 'RWrist',
            'left_hip': 'LHip', 'right_hip': 'RHip',
            'left_knee': 'LKnee', 'right_knee': 'RKnee',
            'left_ankle': 'LAnkle', 'right_ankle': 'RAnkle',
        }
        
        persons = data.get('persons', [])
        person = [p for p in persons if p['id'] == person_id][0]
        
        for frame_num, frame_data in enumerate(person['frames']):
            for keypoint_name, blender_name in keypoint_map.items():
                kp = frame_data['keypoints'].get(keypoint_name)
                if not kp or kp['visible'] == 0:
                    continue
                
                # Coordinate from [0..1] to viewport pixels
                x = kp['x'] * frame_data['width']
                y = kp['y'] * frame_data['height']
                
                # Create or locate empty
                empty_name = f"mtc_{person_id}_{blender_name}"
                if empty_name not in bpy.data.objects:
                    bpy.ops.object.empty_add(
                        type='CIRCLE', size=0.02,
                        align='WORLD', location=(100, 100, 0))
                    empty = bpy.context.active_object
                    empty.name = empty_name
                    empty.display_type = 'SPHERE'
                else:
                    empty = bpy.data.objects[empty_name]
                
                # Set location and keyframe
                empty.location = (x, y, 0)
                empty.keyframe_insert(data_path='location', frame=frame_num)
```

---

## 3. MMPose WORKER (Separate Python Process)

This is not part of the Blender add-on. It's a standalone Python script installed alongside the add-on.

```
motion_tracking/
`-- deps/
   `-- mmpose_worker/
      -- runner.py          -- Entry point
      -- engine.py          -- MMPose model loader (RTMPose or RTMO)
      -- processor.py       -- Frame-by-frame inference
      -- output.py          -- JSON serialization
      `-- requirements.txt
```

### 3.1 Worker Entry Point (runner.py)

```python
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from engine import MMPoseEngine
from processor import VideoProcessor
from output import JSONExporter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Video file or clip filepath')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    parser.add_argument('-m', '--model', default='rtmpose-m', choices=['rtmpose-s', 'rtmpose-m', 'rtmpose-b'])
    parser.add_argument('-d', '--device', default='cpu', choices=['cpu', 'cuda'])
    parser.add_argument('--conf-thresh', type=float, default=0.5)
    parser.add_argument('--multi-person', action='store_true')
    parser.add_argument('--frame-range', nargs=2, type=int, default=[0, -1])
    args = parser.parse_args()
    
    engine = MMPoseEngine(
        model=args.model if args.multi_person else args.model,
        device=args.device,
        conf_thresh=args.conf_thresh,
    )
    
    processor = VideoProcessor(engine, multi_person=args.multi_person)
    exporter = JSONExporter()
    
    frames = processor.run(args.input, frame_range=args.frame_range)
    exporter.write(frames, args.output)
    print(f"Wrote {len(frames)} frames -> {args.output}")

if __name__ == '__main__':
    main()
```

### 3.2 Output Format (JSON)

```json
{
    "video": {
        "filepath": "/path/to/video.mp4",
        "width": 1920,
        "height": 1080,
        "fps": 30
    },
    "model": "rtmpose-m",
    "persons": [
        {
            "id": 0,
            "frames": [
                {
                    "frame": 0,
                    "bbox": [x, y, w, h],
                    "keypoints": {
                        "nose": {"x": 0.45, "y": 0.32, "conf": 0.95, "visible": 1},
                        "left_shoulder": {"x": 0.42, "y": 0.35, "conf": 0.88, "visible": 1},
                        ...
                    }
                },
                ...
            ]
        },
        ...
    ]
}
```

---

## 4. ARMATURE RETARGETING

The add-on creates two armature-mapping presets:

### 4.1 Basic 17-Joint Armature

Maps directly to MMPose's 17 COCO keypoints:

```python
def create_basic_armature(self, person_id):
    bones = ['Root', 'Hip', 'Spine1', 'Spine2', 'Spine3', 
             'Neck', 'Head', 'Nose',
             'LShoulder', 'LElbow', 'LWrist',
             'RShoulder', 'RElbow', 'RWrist',
             'LHip', 'LKnee', 'LAnkle',
             'RHip', 'RKnee', 'RAnkle']
    
    # Parent chain: Hip->Spine1->Spine2->Spine3->Neck->Head->Nose
    # LShoulder->LElbow->LWrist
    # RShoulder->RElbow->RWrist
    # LHip->LKnee->LAnkle
    # RHip->RKnee->RAnkle
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm = bpy.context.active_object.data
    arm.name = f"mtc_arm_{person_id}"
    
    for i, name in enumerate(bones):
        bone = arm.editbones.new(name)
        bone.head = (i * 0.05, 0, 0)
        bone.tail = ((i + 1) * 0.05, 0, 0)
    
    bpy.ops.object.mode_set(mode='POSE')
    return arm
```

### 4.2 Rigify Preset (for production rigs)

```python
def create_rigify_armature(self, person_id):
    """Import existing Rigify armature and apply poses"""
    bpy.ops.object.armature_human_make()
    arm = bpy.data.armatures[f"HumanArmature"]
    
    # Rename to mtc-compatible naming
    bone_aliases = {
        'Head': 'Head', 'Neck': 'Neck',
        'Spine': 'Spine', 'Spine.001': 'Spine1', 'Spine.002': 'Spine2',
        'LArm': 'LShoulder', 'LForeArm': 'LElbow', 'LHand': 'LWrist',
        'RArm': 'RShoulder', 'RForeArm': 'RElbow', 'RHand': 'RWrist',
        'LLeg': 'LHip', 'LSHog': 'LKnee', 'LFoot': 'LAnkle',
        'RLeg': 'RHip', 'RThigh': 'RKnee', 'RFoot': 'RAnkle',
    }
    
    for old, new in bone_aliases.items():
        if old in arm.bones:
            arm.bones[old].name = new
    
    return arm
```

---

## 5. DEVELOPMENT WORKFLOW

### 5.1 Local Development

```bash
# 1. Start Blender with the add-on path
blender \
    --addons /path/to/motion_tracking/ \
    -P /path/to/blender/start_blender.py  # Creates empty scene

# 2. Or use Blender's built-in addon manager
#    Edit -> Preferences -> Add-ons -> Install -> Select the add-on .zip

# 3. Reload hot-reload an active add-on
import importlib
import motion_tracking
importlib.reload(motion_tracking)
```

### 5.2 Testing

```bash
# Test the MMPose worker independently
python deps/mmpose_worker/runner.py \
    -i test_video.mp4 \
    -o output.json \
    -m rtmpose-m \
    -d cpu

# Verify JSON structure
python -c "import json; print(json.dumps(json.load(open('output.json')), indent=2))"

# Verify empties are created correctly
blender --python verify_empties.py  # Custom Python script
```

### 5.3 Distribution

```bash
# Package as .zip for Blender add-on install
zip -r motion_tracking_v0.1.zip \
    motion_tracking/
    # Includes: __init__.py, panel.py, operators.py, deps/
```

Users install via: **Edit -> Preferences -> Add-ons -> Install -> Select .zip**

---

## 6. KEY BLENDER APIs USED

| Task | Blender API |
|---|--|
| UI panel (sidebar) | `bpy.types.Panel` -- `bl_space_type = 'SEQUENCE_EDITOR'` or `'CLIP_EDITOR'` |
| Button properties | `bpy.props.*`: `StringProperty()`, `EnumProperty()`, `BoolProperty()`, `IntProperty()` |
| Create empties | `bpy.ops.object.empty_add(type='CIRCLE', location=...)` |
| Create armature | `bpy.ops.object.armature_add(location=...)` |
| Pose bone animation | `bpy.ops.pose.rotative(orientation='...')` |
| Animation curves | `bpy.data.actions.fcurves` |
| Keyframe insertion | `obj.keyframe_insert(data_path='location', frame=n)` |
| Load video clip | `bpy.data.movieclips.append(filepath)` |
| Get clip frames | `clip.frames` |
| 3D coordinate conversion | `scene.camera.calc_matrix_camera(...)` + `mathutils` |
| Bone/pose manipulation | `bpy.ops.armature.*`, `bpy.ops.pose.*` |
| Preferences UI | `bpy.types.AddonPreferences` |

---

## 7. INTEGRATION FLOW

```
                    Developer                    Blender User
                        |                          |
                        v                          v
                 +--+----+------+          +--+----+------+
                 | Blender Add-on|          | Video Source  |
                 | (pure Python) |          | (.mp4, .mov)  |
                 +--+----+------+          +--+----+------+
                    |   User loads video into
                    |   Video/Clip Editor
                    v                          |
                 +--+----+------+             |
                 |  Panel UI    |<------+----+
                 |  (Sidebar)   |
                 +--+----+------+
                    |   User clicks "Run Inference"
                    v
                 +--+----+------+
                 | subprocess   |  Blender calls MMPose worker
      -----+----| (Python)   |+---- as a separate process
                 |              |
                 | MMPose/RTMO  |  Detects people + keypoints
                 +--+----+------+
                    |
                    v
                 +--+----+------+
                 |   JSON output|
                 +--+----+------+
                    |
                    v
                 +--+----+------+
                 | Import to    |   Maps keypoints + empties/bones
                 | Blender      |   + keyframes per time
                 +--+----+------+
                    |
                    v
                 +--+----+------+
                 |  Armature    |   User applies to existing Rigify/armature
                 |  animation   |
                 +--+----+------+
```

---

## 8. CRITICAL NOTES

### 8.1 Coordinate System Mismatch

- **MMPose:** Origin top-left, x = [0..1], y = [0..1]
- **Blender:** Origin = video center, y is up
- **Fix:** Convert in processors.py:
  ```python
  # 0..1 -> -1..1
  x_blender = (kp_x - 0.5) * clip.width / 2
  y_blender = (kp_y - 0.5) * clip.height / 2
  ```

### 8.2 Out-of-Box Architecture

**The add-on NEVER imports MMPose modules.** It communicates via:
1. **File:** writes JSON to disk -> reads JSON
2. **Subprocess:** launches `python deps/mmpose_worker/runner.py`

This means:
- Blender users don't need Torch/CUDA installed -- MMPose worker handles its own environment
- No cross-compilation
- No Python version conflicts

### 8.3 Video Editor vs Clip Editor

- **Video Editor (Sequencer):** `bl_space_type = 'SEQUENCE_EDITOR'` -- for timeline-based workflow
- **Clip Editor (Motion Tracking):** `bl_space_type = 'CLIP_EDITOR'` -- for manual tracking
- **Our panel goes in CLIP_EDITOR** since users load video into the Clip Editor for tracking.

---

## 9. NEXT STEPS

1. **File:** Create the directory structure per section 1
2. **Worker:** Finish `deps/mmpose_worker/` (engine, processor, output)
3. **Panel:** Implement `panel.py` with all UI elements
4. **Operators:** Implement `operators.py` with inference + import
5. **Mapping:** Implement armature mapping presets
6. **Test:** Verify end-to-end with a sample video
7. **Package:** Zip and distribute
