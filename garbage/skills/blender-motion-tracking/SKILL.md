# Blender Motion Tracking Add-on

## Trigger
When the user asks about:
- Building, writing, or debugging a Blender add-on for motion tracking / pose detection
- Integrating MMPose / RTMPose / RTMO into Blender
- Creating Blender armature animations from video pose data
- Converting keypoint coordinate systems between MMPose and Blender
- Distributing Blender add-ons

## Context
This project targets **Blender 4.2+** using a **pure Python add-on** — no C++, no Pybind11, no TorchScript wrapping.

## Core Architecture

The deliverable is a pure-Python Blender add-on that communicates with a separate MMPose worker subprocess:

```
addons/
motion_tracking/                    <- Blender add-on (pure Python)
   +-- __init__.py                  <- Entry point: bl_info, register, unregister
   +-- panel.py                     <- UI panel in Clip Editor sidebar
   +-- operators.py                 <- Run inference, import results
   +-- retarget.py                  <- Armature mapping presets
   +-- deps/
      +-- mmpose_worker/            <- Standalone MMPose pipeline
         +-- runner.py              <- Entry point
         +-- engine.py              -> MMPose model loader
         +-- processor.py           -> Frame-by-frame inference
         +-- output.py              -> JSON serialization
         +-- requirements.txt
```

## Key Design Decisions

1. **Pure Python** — Blender embeds Python. MMPose is Python-native. No C++ toolchain needed.
2. **Out-of-process** — The add-on launches `python deps/mmpose_worker/runner.py` as a subprocess and reads JSON output. Users never need Torch/CUDA installed locally.
3. **Thin add-on layer** — Only handles UI + data mapping. MMPose does all inference.
4. **Panel lives in `CLIP_EDITOR`** — `bl_space_type = 'CLIP_EDITOR'` for the tracking workflow.

## Workflow

1. User loads video into the Clip Editor
2. Panel appears in sidebar with: video path selector, model choice, device selection, person selector
3. User clicks "Run Inference" -> add-on launches MMPose subprocess
4. MMPose writes JSON output with detected keypoints per frame
5. User clicks "Import" -> add-on maps keypoints to Blender empties with keyframes
6. User clicks "Create Armature" -> add-on creates bone structure (basic 17-joint or Rigify preset)
7. Poses are applied to armature bones frame-by-frame

## Coordinate Conversion

MMPose origin is top-left (0..1 normalized). Blender origin is video center. Convert in the add-on:

```python
x_blender = (kp_x - 0.5) * clip.width / 2
y_blender = (kp_y - 0.5) * clip.height / 2
```

## MMPose Output Format

```json
{
    "video": {"filepath": "...", "width": 1920, "height": 1080, "fps": 30},
    "model": "rtmpose-m",
    "persons": [{
        "id": 0,
        "frames": [{
            "frame": 0,
            "bbox": [x, y, w, h],
            "keypoints": {
                "nose": {"x": 0.45, "y": 0.32, "conf": 0.95, "visible": 1},
                "left_shoulder": {"x": 0.42, "y": 0.35, "conf": 0.88, "visible": 1}
            }
        }]
    }]
}
```

## MMPose Keypoint Names (COCO 17)

nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle

## Key Blender APIs

| Task | API |
|---|- -- |
| UI panel | `bpy.types.Panel` with `bl_space_type = 'CLIP_EDITOR'` |
| Properties | `bpy.props.String/Enum/Bool/IntProperty()` |
| Empties | `bpy.ops.object.empty_add()` |
| Armature | `bpy.ops.object.armature_add()` |
| Keyframes | `obj.keyframe_insert(data_path='location', frame=n)` |
| Clips | `bpy.data.movieclips.append(filepath)`, `clip.frames` |
| Bones | `arm.editbones.new(name)`, bone.head/tail |
| Reload | `import importlib; importlib.reload(module)` |

## Distribution

Package as `.zip` for Blender add-on install: Edit -> Preferences -> Add-ons -> Install -> Select .zip
