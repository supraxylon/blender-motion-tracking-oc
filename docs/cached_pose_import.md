# Cached Pose Import

WI-003 uses a cached JSON file as the handoff between the external pose worker and Blender.

## Flow

1. Produce or receive a tracking result JSON that follows `schemas/tracking_result.schema.json`.
2. Check it with:

   ```powershell
   python tools/validate_tracking_json.py examples/sample_tracking_result.json
   ```

3. In Blender, install or load `src/blender_pose_tracker` as the add-on package.
4. Use the Pose Tracker sidebar panel to choose the cached JSON file and import pose empties.

The sample file at `examples/sample_tracking_result.json` is the smallest practical fixture for this flow. It should remain valid against the schema and usable by the importer.

## Local Blender

A local Blender 5.1 build is present at:

```text
blender/blender-5.1.1-windows-x64/blender-5.1.1-windows-x64/blender.exe
```

If system `python` is not available, Blender also includes a bundled Python interpreter under the same local Blender folder.

## Smoke Check

Run the lightweight smoke check from the repo root:

```powershell
python tests/smoke_validate_cached_pose.py
```

If `python` is not on PATH, use Blender's bundled Python:

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tests\smoke_validate_cached_pose.py
```

It uses only the Python standard library. It checks that the schema, sample JSON, validator, and add-on files exist; runs the validator with the current Python executable; compiles the add-on Python files; and notes whether `test_data/green_field.mp4` exists without processing it.

`test_data/green_field.mp4` is ready for the next milestone: the external MMPose worker that turns video into cached JSON.
