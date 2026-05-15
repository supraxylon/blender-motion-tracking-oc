# MVP Evaluation

## What the MVP Currently Proves

1. **Fixture worker path works end-to-end.**
   `tracking_worker.cli` accepts `--input`, `--output`, `--backend fixture`, writes schema-compatible JSON, and validates.

2. **JSON schema validation works.**
   `tools/validate_tracking_json.py` accepts the output and confirms structure compliance.

3. **Fixture and backend-readiness test suite passes.**
   `tests/test_tracking_worker_fixture.py` confirms fixture behavior and clear RTMPose missing-dependency failure with Blender bundled Python.

4. **Visual preview works from cached JSON.**
   `tools/render_tracking_preview.py` renders `<line>`, `<circle>`, `<rect>` skeletons from `outputs/green_field_tracking.json` to SVG.

5. **Runtime probe confirms bundled Python runs.**
   Blender's bundled Python 3.13.9 imports `tracking_worker.cli` and executes commands.

6. **Test video exists as source.**
   `test_data/green_field.mp4` (~282 MB) is present for the worker input path.

## What the MVP Does NOT Prove

- No real pose inference has run on any video. Fixture output is synthetic.
- `green_field.mp4` pixels have not been analyzed.
- RTMPose / MMPose / torch / OpenCV are not installed in any environment.
- Blender runtime (`blender.exe`) does not launch on this machine (Windows SxS error).
- `ffmpeg` / `ffprobe` are not installed, so real video metadata extraction has not been tested.
- Real MOT (ByteTrack), object masks (SAM 2), and 3D lift (WHAM) are untested.
- No identity consistency, accuracy, or latency benchmarks exist.

## Exact Commands

### Fixture worker (uses cached synthetic data only)

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
```

### Schema validation

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\validate_tracking_json.py outputs\green_field_tracking.json
```

### Fixture test suite

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\test_tracking_worker_fixture.py
```

### SVG preview (visual inspection of cached data)

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\render_tracking_preview.py --input outputs\green_field_tracking.json --output outputs\green_field_tracking_preview.svg
```

### Runtime probe

```powershell
powershell -ExecutionPolicy Bypass -File tools\probe_blender_runtime.ps1
```

## Preview SVG

`outputs/green_field_tracking_preview.svg`

Open it in any browser to inspect the cached fixture skeleton layout.
