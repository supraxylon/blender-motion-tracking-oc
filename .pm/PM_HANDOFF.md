# PM Handoff

Purpose: let any future agent take over as project manager without re-discovering the whole repo.

## Current Role

You are the PM/orchestrator unless the user explicitly asks you to implement.

Your job:
- Keep work aligned to the plan.
- Split work into concrete work items.
- Delegate when useful.
- Verify deliverables before claiming progress.
- Keep `.pm/STATUS.md`, stand-ups, backlog, and decision log current.
- Do not silently install heavy dependencies.
- Do not delete files directly; move removals to `garbage/`.

## Project Direction

Canonical planning docs:
- `docs/PROJECT_VISION.md`
- `PLAN.md`
- `documentation/PLAN.md`
- `deep-research-report.md`
- `.pm/PLAN_SUMMARY.md`
- `.pm/BACKLOG.md`

Active architecture:

```text
video
-> external RTMPose/MMPose worker
-> cached tracking JSON
-> Blender add-on import
-> keypoint empties / overlays
-> later armature retargeting
```

Important decision:
- RTMPose/MMPose is the v1 pose backend direction.
- LoRATv2 is research/backup for box, object, or camera tracking, not the v1 pose backend.
- Heavy ML inference stays outside Blender.

## Current State

Completed:
- WI-003: cached pose JSON importer MVP.
- WI-004: external worker fixture MVP.
- WI-005: MVP evaluation pack.
- WI-006: real pose backend readiness.

Current milestone:
- Milestone 003 complete.

Next work item:
- `WI-007 - First Real RTMPose Attempt`
- Start with `.pm/tasks/WI-007-A.md`.

Do not begin WI-007-B dependency installation until the user approves the install approach.

Latest housekeeping report:
- `.pm/reports/HOUSEKEEPING-2026-05-12.md`

OpenCode skill:
- `.pm/skills/opencode-orchestrator/SKILL.md`
- Use this skill when delegating work to OpenCode or when repairing OpenCode delegation/reporting.

## What Works

- `tracking_worker.cli --backend fixture` writes cached tracking JSON.
- `tools/validate_tracking_json.py` validates generated JSON.
- `tests/test_tracking_worker_fixture.py` passes.
- `tests/smoke_validate_cached_pose.py` passes.
- `tools/render_tracking_preview.py` creates an SVG pose preview.
- `tracking_worker.cli --backend rtmpose` is recognized and fails clearly when dependencies are missing.

## What Does Not Work

- No real RTMPose/MMPose inference has run.
- `test_data/green_field.mp4` has not been analyzed by real pose tracking.
- Repo-local `blender.exe` fails with a Windows side-by-side configuration error.
- `ffmpeg` / `ffprobe` are not on PATH.
- RTMPose/MMPose/torch/OpenCV are not installed in the validated environment.

## Validation Commands

Use Blender bundled Python from the repo:

```powershell
$py = Resolve-Path 'blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe'
```

Smoke test:

```powershell
& $py -S tests\smoke_validate_cached_pose.py
```

Worker fixture test:

```powershell
& $py -S tests\test_tracking_worker_fixture.py
```

Generate fixture JSON:

```powershell
& $py -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_tracking.json --backend fixture
```

Validate JSON:

```powershell
& $py -S tools\validate_tracking_json.py outputs\green_field_tracking.json
```

Render preview:

```powershell
& $py -S tools\render_tracking_preview.py --input outputs\green_field_tracking.json --output outputs\green_field_tracking_preview.svg
```

Expected RTMPose placeholder failure:

```powershell
& $py -S -m tracking_worker.cli --input test_data\green_field.mp4 --output outputs\green_field_rtmpose.json --backend rtmpose
```

Expected result: non-zero exit with a clear missing-dependency message.

## OpenCode Notes

OpenCode server URL used so far:

```text
http://localhost:4096
```

Known session:

```text
ses_1e5bc0f9dffeg2J57Yu13nCMhc
```

Use `opencode run --attach`; do not use `opencode attach` because that opens the TUI.

If OpenCode fails with a config path issue, redirect config into `.pm` for the command:

```powershell
$env:XDG_CONFIG_HOME = (Resolve-Path '.pm').Path + '\opencode-config'
opencode run --attach http://localhost:4096 "<task>"
```

If OpenCode creates runtime state under `.pm/opencode-home` or `.pm/opencode-config`, keep those out of active PM records. They are ignored and may be moved to `garbage/`.

## Cleanup Rules

- Never delete directly.
- Move superseded files to `garbage/<clear-folder-name>/`.
- Keep project docs canonical; avoid multiple root-level status summaries.
- Current unified status/vision lives in `docs/PROJECT_VISION.md`.
- Current PM state lives in `.pm/STATUS.md`.
- Current stand-up lives in `.pm/standups/2026-05-12.md`.

Already archived:
- OpenCode runtime state: `garbage/opencode-runtime-20260512-101539/`
- Superseded root summaries: `garbage/markdown-consolidation-20260512/`

Important git-status note:
- `.pm/opencode-home/` contained tracked generated runtime files. They were moved to `garbage/`, so git may show many deletions under `.pm/opencode-home/`. This is expected cleanup state, not data loss.

## PM Operating Loop

1. Read `.pm/STATUS.md`.
2. Read this file.
3. If using OpenCode, read `.pm/skills/opencode-orchestrator/SKILL.md`.
4. Read the active work item and task files.
5. Confirm the current blocker or next task.
6. Delegate or implement only the scoped task.
7. Run validation.
8. Update `.pm/STATUS.md`.
9. Update `.pm/standups/YYYY-MM-DD.md`.
10. Add any architecture decision to `.pm/DECISIONS.md`.
11. Create a short report under `.pm/reports/`.

## WI-007 Guidance

WI-007 should not start by installing packages.

First task:
- `.pm/tasks/WI-007-A.md`

Deliverable:
- `.pm/reports/WI-007-A-env-plan.md`

The report should:
- Identify available Python environment options.
- Recommend one external environment path.
- Separate CPU-only and CUDA options.
- List the exact commands that require user approval.

Only after approval should WI-007-B install or probe RTMPose/MMPose dependencies.

## Final Handoff Note

Be strict about claims:
- Say fixture when output is synthetic.
- Say real inference only after video pixels are actually processed.
- Say Blender validation only after `blender.exe` launches or another working Blender install is used.
