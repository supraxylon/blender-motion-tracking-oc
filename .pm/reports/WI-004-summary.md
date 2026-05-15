# WI-004 Summary - External Worker Foundation

Status: complete for fixture MVP.

## What Works

- `tracking_worker.cli` runs with `--input`, `--output`, and `--backend fixture`.
- The worker writes `outputs/green_field_tracking.json`.
- The generated output validates against the current schema rules.
- `tests/test_tracking_worker_fixture.py` passes with Blender's bundled Python in `-S` mode.
- `docs/external_worker.md` documents the real command path and fixture limitation.
- `test_data/green_field.mp4` is present and usable as the source path.

## What Does Not Work

- No real pose inference has run.
- Fixture output is synthetic; it does not inspect the video pixels.
- Local `blender.exe` still fails with a Windows side-by-side configuration error.
- `ffmpeg` / `ffprobe` are not available in PATH.
- RTMPose/MMPose/torch/OpenCV are not installed.

## Blockers

- Need a usable real-inference environment before converting `green_field.mp4` to true pose tracks.
- Need Blender runtime launch fixed before full add-on validation inside Blender.
- Need choose whether next real backend is RTMPose/MMPose first or LoRATv2 C++ bridge research first.

## Validation Run

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
```

Result:
- Worker wrote 2 frames / 2 total person observations.
- Schema validation passed.
- Seven fixture worker checks passed.

## Artifacts

| File | Purpose |
| --- | --- |
| `tracking_worker/cli.py` | Worker command entry point. |
| `tracking_worker/fixture_backend.py` | Synthetic COCO-17 fixture backend. |
| `tracking_worker/schema_io.py` | Schema-aware read/write/validation helper. |
| `tests/test_tracking_worker_fixture.py` | Plain-assert worker validation. |
| `outputs/green_field_tracking.json` | Generated fixture output for the test video path. |
| `docs/external_worker.md` | Usage doc. |

## Recommendation

Next work item should make the MVP evaluable: generate a visible preview from `outputs/green_field_tracking.json`, then repair/verify Blender launch separately so the same cached output can be inspected in Blender.
