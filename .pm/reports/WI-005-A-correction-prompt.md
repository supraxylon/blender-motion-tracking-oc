# WI-005-A Correction Prompt

Fix only `tools/render_tracking_preview.py`.

Problem:
- The command runs and writes `outputs/green_field_tracking_preview.svg`.
- The SVG contains `<svg>` and the background `<rect>`.
- It does not contain pose `<circle>` or skeleton `<line>` elements because generated draw elements are not inserted into the SVG.

Required fix:
- Insert the generated pose/bbox/skeleton elements into the SVG before closing it.
- Keep stdlib only.
- Keep the same CLI.
- Regenerate `outputs/green_field_tracking_preview.svg`.

Acceptance:
- This command succeeds:
  `.\blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe -S tools\render_tracking_preview.py --input outputs\green_field_tracking.json --output outputs\green_field_tracking_preview.svg`
- `outputs/green_field_tracking_preview.svg` contains `<circle`.
- `outputs/green_field_tracking_preview.svg` contains `<line`.

Return final report with files changed, commands run, validation, blockers, next task.
