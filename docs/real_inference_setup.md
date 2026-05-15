# Real Inference Setup

## Purpose

This is the next practical step after the fixture MVP: run RTMPose/MMPose outside Blender and write the same cached JSON format the Blender add-on already understands.

No heavy dependencies were installed during WI-006.

## Current Worker Behavior

Fixture backend:

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
```

RTMPose placeholder:

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_rtmpose.json --backend rtmpose
```

Expected today: non-zero exit with a clear missing-dependency message for PyTorch, OpenCV, MMEngine, MMCV, and MMPose.

## Required External Tools

- A normal Python environment outside Blender.
- PyTorch appropriate for CPU or CUDA.
- OpenCV.
- OpenMMLab packages: MMEngine, MMCV, MMPose.
- FFmpeg or another video reader for reliable FPS/duration/frame metadata.
- RTMPose model config and checkpoint.

## Intended Setup Shape

```text
repo
-> tracking_worker
-> external Python env
   -> torch
   -> opencv
   -> mmengine/mmcv/mmpose
   -> RTMPose config/checkpoint
-> outputs/*.json
-> Blender imports cached JSON
```

## Intended Evaluation Commands

These are not runnable until the external environment is created:

```powershell
python -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_rtmpose.json --backend rtmpose
python tools\validate_tracking_json.py outputs\green_field_rtmpose.json
python tools\render_tracking_preview.py --input outputs\green_field_rtmpose.json --output outputs\green_field_rtmpose_preview.svg
```

## Current Blockers

- Blender executable fails locally with a Windows side-by-side configuration error.
- `ffmpeg` and `ffprobe` are not on PATH.
- RTMPose/MMPose/torch/OpenCV are not installed.
- The current `rtmpose` backend is a dependency-aware placeholder, not real inference.

## Next Executable Step

Create an isolated external Python environment for RTMPose/MMPose, then replace the placeholder `tracking_worker/backends/rtmpose.py` with a minimal real inference path that writes the existing schema.
