# WI-006 Summary - Real Pose Backend Readiness

Status: complete.

## Delivered

- `tracking_worker/backends/` backend registry.
- Fixture backend adapter under `tracking_worker/backends/fixture.py`.
- Safe RTMPose placeholder under `tracking_worker/backends/rtmpose.py`.
- CLI support for `--backend fixture` and `--backend rtmpose`.
- Test coverage for fixture success and RTMPose missing-dependency failure.
- `docs/real_inference_setup.md`.
- `docs/PROJECT_VISION.md`.
- `.pm/PM_HANDOFF.md`.
- `.pm/reports/HOUSEKEEPING-2026-05-12.md`.

## What Works

- Fixture backend still writes valid cached JSON.
- `--backend rtmpose` exits non-zero with a useful missing-dependency message.
- No heavy ML dependencies were installed.
- Existing validation commands still pass.

## What Does Not Work

- Real RTMPose inference is not implemented yet.
- Real video pixels have not been analyzed.
- Blender runtime still does not launch locally.

## Validation

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_rtmpose.json --backend rtmpose
```

Result:
- Fixture tests passed.
- Fixture output validated.
- RTMPose command failed clearly because dependencies are missing.

## Cleanup

- Generated OpenCode runtime state was moved to `garbage/opencode-runtime-20260512-101539/`.

## Next Milestone

WI-007 should create the external Python/RTMPose environment and run the first real inference attempt on `test_data/green_field.mp4`.

Start with WI-007-A and do not install heavy dependencies before approval.
