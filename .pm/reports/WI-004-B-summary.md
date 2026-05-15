# WI-004-B Summary - Worker CLI Scaffold

Status: complete after Codex validation pass.

## Deliverables

- `tracking_worker/cli.py`
- `tracking_worker/fixture_backend.py`
- `tracking_worker/schema_io.py`
- `tests/test_tracking_worker_fixture.py`
- `outputs/green_field_tracking.json`

## What Works

- Fixture backend creates schema-compatible cached pose JSON.
- CLI accepts input video path, output path, and backend name.
- Output validates before write.
- Test harness now runs under Blender bundled Python with `-S`.

## What Changed During Review

- Codex converted the test harness from `unittest` to plain assertions because `unittest` was unavailable in Blender bundled Python `-S` mode.
- Product worker files were left scoped to the fixture backend.

## Validation

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
```

Result: all passed.

## Not Done

- Real tracking inference.
- Video pixel analysis.
- Blender runtime validation.
