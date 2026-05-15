# WI-005-B Report - Blender Runtime Probe

Date: 2026-05-12  
Status: complete and locally verified.

## Deliverables

| File | Purpose |
| --- | --- |
| `tools/probe_blender_runtime.ps1` | Local runtime probe script. |
| `.pm/reports/WI-005-B-probe-raw.txt` | Raw probe output from Codex validation. |
| `.pm/reports/WI-005-B-blender-runtime-probe.md` | This summary. |

## What Works

- Repo-local bundled Python exists and runs: Python 3.13.9.
- Bundled Python can import `tracking_worker.cli`.
- `test_data/green_field.mp4` exists, about 282.63 MB.
- `outputs/green_field_tracking.json` exists.

## What Does Not Work

- Repo-local `blender.exe` exists but fails with a Windows side-by-side configuration error.
- `python`, `python3`, `blender`, `ffprobe`, and `ffmpeg` are not available on PATH in the validated shell.

## Validation Command

```powershell
powershell -ExecutionPolicy Bypass -File tools\probe_blender_runtime.ps1
```

Result: probe completed; Blender launch failed; bundled Python worked.

## Blockers

- Blender runtime launch is blocked by Windows SxS dependency/configuration failure.
- Video metadata and future real inference still need FFmpeg/ffprobe or another approved video stack.
- Real pose inference still needs RTMPose/MMPose/torch/OpenCV in a separate external environment.

## Next Task

Use `outputs/green_field_tracking_preview.svg` for visual inspection while Blender runtime launch is unresolved.
