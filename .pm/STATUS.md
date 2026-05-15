# PM Status

## Current Phase
Milestone 003 - Real pose backend readiness.

## Current Work Item
WI-006 - Real Pose Backend Readiness.

## Current Task
Housekeeping complete. WI-007 queued.

## OpenCode Server URL
`http://localhost:4096`

## OpenCode Session ID
`ses_1e5bc0f9dffeg2J57Yu13nCMhc`

## Last Completed Task
PM handoff and housekeeping completed after WI-006-C.

## What Works
- Cached pose schema, sample, validator, Blender add-on skeleton, and smoke test exist.
- External worker fixture backend exists.
- `outputs/green_field_tracking.json` was generated from the green-field video path.
- Worker output validates.
- Worker tests pass with Blender bundled Python.
- `outputs/green_field_tracking_preview.svg` exists and contains pose geometry.
- Runtime probe confirms bundled Python works and repo-local Blender launch fails.
- Backend registry exists.
- `--backend rtmpose` fails clearly with missing dependency details.
- PM handoff exists at `.pm/PM_HANDOFF.md`.
- OpenCode delegation skill exists at `.pm/skills/opencode-orchestrator/SKILL.md`.
- Unified project vision exists at `docs/PROJECT_VISION.md`.

## What Does Not Work
- `python`, `blender`, `ffmpeg`, and `ffprobe` are not available on PATH in this shell.
- Repo-local `blender.exe` fails to launch with a Windows side-by-side configuration error.
- No real RTMPose/MMPose/LoRAT inference has run.
- OpenCode runtime state was moved out of `.pm/` into `garbage/`.

## Blockers
- Blender runtime launch must be fixed before full in-Blender validation.
- Real inference requires a separate Python/ML environment or approved dependency install.

## Next Recommended Action
Run WI-007-A: choose the external Python environment path before installing RTMPose/MMPose dependencies.

## Source Plan Read Status
- `documentation/PLAN.md`: read successfully by Codex.
- `deep-research-report.md`: read successfully by Codex.

## Deliverable Status
- `.pm/PLAN_SUMMARY.md`: created.
- `.pm/BACKLOG.md`: created.
- `.pm/DECISIONS.md`: created.
- `.pm/PROJECT_BRIEF.md`: created.
- `.pm/work_items/WI-002.md`: created.
- `.pm/MILESTONE-001.md`: created.
- `.pm/work_items/WI-003.md`: created.
- `schemas/tracking_result.schema.json`: created.
- `examples/sample_tracking_result.json`: created.
- `tools/validate_tracking_json.py`: created.
- `src/blender_pose_tracker/__init__.py`: created.
- `src/blender_pose_tracker/importer.py`: created.
- `docs/cached_pose_import.md`: created.
- `tests/smoke_validate_cached_pose.py`: passes.
- `.pm/STANDUP.md`: created.
- `.pm/standups/2026-05-12.md`: updated.
- `.pm/MILESTONE-002.md`: created.
- `.pm/work_items/WI-004.md`: created.
- `.pm/tasks/WI-004-A.md`: created.
- `.pm/tasks/WI-004-B.md`: created.
- `.pm/tasks/WI-004-C.md`: created.
- `.pm/reports/WI-004-A-env-video-probe.md`: created.
- `.pm/reports/WI-004-B-summary.md`: created.
- `.pm/reports/WI-004-summary.md`: created.
- `tracking_worker/cli.py`: created.
- `tracking_worker/fixture_backend.py`: created.
- `tracking_worker/schema_io.py`: created.
- `tests/test_tracking_worker_fixture.py`: passes.
- `outputs/green_field_tracking.json`: generated and validated.
- `docs/external_worker.md`: updated.
- `.pm/work_items/WI-005.md`: created.
- `.pm/tasks/WI-005-A.md`: created.
- `.pm/tasks/WI-005-B.md`: created.
- `.pm/tasks/WI-005-C.md`: created.
- `tools/render_tracking_preview.py`: created.
- `outputs/green_field_tracking_preview.svg`: generated.
- `tools/probe_blender_runtime.ps1`: created.
- `.pm/reports/WI-005-A-summary.md`: created.
- `.pm/reports/WI-005-B-blender-runtime-probe.md`: created.
- `.pm/reports/WI-005-B-probe-raw.txt`: created.
- `docs/mvp_evaluation.md`: created.
- `.pm/reports/WI-005-summary.md`: created.
- `.pm/work_items/WI-006.md`: completed.
- `.pm/tasks/WI-006-A.md`: completed.
- `.pm/tasks/WI-006-B.md`: completed.
- `.pm/tasks/WI-006-C.md`: completed.
- `.pm/MILESTONE-003.md`: completed.
- `tracking_worker/backends/`: created.
- `tracking_worker/backends/rtmpose.py`: created.
- `docs/real_inference_setup.md`: created.
- `docs/PROJECT_VISION.md`: created.
- `.pm/reports/WI-006-summary.md`: created.
- `.pm/work_items/WI-007.md`: queued.
- `.pm/tasks/WI-007-A.md`: queued.
- `.pm/tasks/WI-007-B.md`: queued.
- `.pm/tasks/WI-007-C.md`: queued.
- `garbage/opencode-runtime-20260512-101539/`: archived generated OpenCode runtime state.
- `garbage/markdown-consolidation-20260512/`: archived superseded root summary/report markdown.
- `.pm/PM_HANDOFF.md`: created.
- `.pm/skills/opencode-orchestrator/SKILL.md`: created.
- `.pm/reports/OPENCODE-SKILL-2026-05-12.md`: created.
- `.pm/reports/HOUSEKEEPING-2026-05-12.md`: created.
