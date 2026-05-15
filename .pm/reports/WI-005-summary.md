# WI-005 Summary - MVP Evaluation Pack

Status: complete.

## Deliverables

| File | Purpose |
| --- | --- |
| `tools/render_tracking_preview.py` | Stdlib JSON-to-SVG preview tool. |
| `outputs/green_field_tracking_preview.svg` | Visual preview of cached pose data. |
| `tools/probe_blender_runtime.ps1` | Runtime/environment probe. |
| `.pm/reports/WI-005-B-probe-raw.txt` | Raw probe output. |
| `docs/mvp_evaluation.md` | What the MVP proves, does not prove, and exact commands. |
| `.pm/reports/WI-005-A-summary.md` | Preview branch report. |
| `.pm/reports/WI-005-B-blender-runtime-probe.md` | Runtime probe report. |
| `.pm/standups/2026-05-12.md` | Stand-up update. |

## What Works

- Worker fixture output validates.
- Worker fixture and backend-readiness tests pass.
- Cached pose smoke test passes cleanly.
- SVG preview contains frame, skeleton lines, keypoint circles, labels, and track ID.
- Bundled Python works for validation and worker commands.

## What Does Not Work

- No real pose inference has run.
- Fixture output is synthetic and does not inspect video pixels.
- Repo-local `blender.exe` fails with Windows side-by-side configuration error.
- `python`, `blender`, `ffmpeg`, and `ffprobe` are not available on PATH in the validated shell.

## Validation

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\smoke_validate_cached_pose.py
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\render_tracking_preview.py --input outputs\green_field_tracking.json --output outputs\green_field_tracking_preview.svg
powershell -ExecutionPolicy Bypass -File tools\probe_blender_runtime.ps1
```

Result: all completed; Blender launch failure remains documented in the probe output.

## Next Task

WI-006 is now complete. Next: run WI-007-A to choose the external Python environment path.
