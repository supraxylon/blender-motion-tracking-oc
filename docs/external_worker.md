# External Worker Usage

## Purpose

`tracking_worker` is the external video-to-JSON path for v1.
It keeps heavy tracking work outside Blender and writes schema-compatible cached pose data for the Blender importer.

## Current Backends

Implemented worker backend paths:
- `fixture`: working synthetic data backend for plumbing validation.
- `rtmpose`: recognized placeholder that fails clearly until external ML dependencies are installed.

The fixture backend is useful for plumbing tests only:
- It reads the input path for metadata.
- It writes two synthetic frames.
- Each frame contains one tracked person with 17 COCO keypoints.
- It does not perform real pose estimation on `test_data/green_field.mp4`.

## Run

```powershell
python -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
```

When using Blender's bundled Python from this repo:

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
```

## Validate

```powershell
python tools\validate_tracking_json.py outputs\green_field_tracking.json
python tests\test_tracking_worker_fixture.py
```

Blender bundled Python version:

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
```

## Output Contract

The worker writes `schemas/tracking_result.schema.json` compatible JSON:

| Field | Meaning |
| --- | --- |
| `video_meta.width` / `video_meta.height` | Source dimensions used by the worker. |
| `video_meta.fps` / `video_meta.duration` | Optional timing metadata. |
| `video_meta.source` | Source video path. |
| `frames[].frame_index` | Zero-based frame index. |
| `frames[].width` / `frames[].height` | Per-frame dimensions. |
| `frames[].persons[]` | Tracked people in the frame. |
| `persons[].track_id` | Stable identity, or `null` if unassigned. |
| `persons[].keypoints[]` | Exactly 17 normalized COCO keypoints. |
| `persons[].bbox` | Normalized bounding box. |

## Known Limits

- Fixture output is synthetic and should not be judged as tracking quality.
- Real RTMPose/MMPose inference is not installed or implemented yet.
- Local `blender.exe` still needs launch repair before full in-Blender validation.

## Real Backend Readiness

See `docs/real_inference_setup.md`.
