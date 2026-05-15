# WI-003 MVP Summary

Status: MVP delivered for evaluation.

Feature:
- Cached pose JSON -> Blender add-on -> keyed empties.

Created:
- `schemas/tracking_result.schema.json`
- `examples/sample_tracking_result.json`
- `tools/validate_tracking_json.py`
- `src/blender_pose_tracker/__init__.py`
- `src/blender_pose_tracker/importer.py`
- `docs/cached_pose_import.md`
- `tests/smoke_validate_cached_pose.py`

Validation:
- Sample JSON validator passes.
- Bad keypoint count fails.
- Add-on files compile.
- Smoke check passes with Blender bundled Python:
  `.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\smoke_validate_cached_pose.py`

Known blocker:
- Local `blender.exe` failed to start with a Windows side-by-side configuration error. Full headless Blender import was not run here.

Video:
- `test_data/green_field.mp4` exists.
- It is reserved for the next milestone: external MMPose worker -> cached JSON.

Next:
- Build the video-to-JSON worker for `test_data/green_field.mp4`.
