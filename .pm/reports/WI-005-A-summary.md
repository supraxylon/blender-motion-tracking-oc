# WI-005-A Summary - Cached Pose SVG Preview

Status: complete after correction.

## Deliverables

| File | Purpose |
| --- | --- |
| `tools/render_tracking_preview.py` | Stdlib-only JSON-to-SVG preview tool. |
| `outputs/green_field_tracking_preview.svg` | Human-viewable preview of cached pose output. |
| `.pm/reports/WI-005-A-correction-prompt.md` | Correction sent after blank SVG validation failure. |

## What Works

- Preview command runs with Blender bundled Python in `-S` mode.
- SVG contains frame box, skeleton lines, keypoint circles, labels, and track ID.
- COCO-17 skeleton mapping now uses the schema's keypoint order.

## Validation

```powershell
.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\render_tracking_preview.py --input outputs\green_field_tracking.json --output outputs\green_field_tracking_preview.svg
```

Result: output written; SVG contains `<line`, `<circle`, and `<rect`.

## What Does Not Work

- Preview uses cached fixture data only.
- It does not draw over the original video frame.
- It does not prove real tracking quality.
