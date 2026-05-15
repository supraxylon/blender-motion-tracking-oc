# Housekeeping Report - 2026-05-12

## Purpose

Document the PM cleanup and make the next step obvious for any agent taking over.

## Work Completed

- Created `.pm/PM_HANDOFF.md` as the project-manager takeover document.
- Created `.pm/skills/opencode-orchestrator/SKILL.md` as the OpenCode delegation skill.
- Linked the PM handoff from `README.md` and `AGENTS.md`.
- Linked the OpenCode skill from `README.md`, `AGENTS.md`, and `.pm/PM_HANDOFF.md`.
- Added `.pm/reports/OPENCODE-SKILL-2026-05-12.md`.
- Ignored `.codex/` after the skill initializer created a write-protected scaffold there.
- Updated `.pm/STATUS.md` with current state, completed WI-006 work, and WI-007 next action.
- Updated `.pm/standups/2026-05-12.md` with the PM handoff and housekeeping pass.
- Updated `.pm/BACKLOG.md` with execution status and the current WI-007-A next action.
- Updated `docs/PROJECT_VISION.md` with the current PM plan.
- Cleaned `.pm/DECISIONS.md` so the backend registry decision is ADR-5 instead of conflicting with earlier ADR numbering.

## Current Plan

Next work item:
- `WI-007 - First Real RTMPose Attempt`

Next task:
- `WI-007-A - External Environment Plan`

Deliverable:
- `.pm/reports/WI-007-A-env-plan.md`

WI-007-A must choose a safe external Python environment path and list install commands that require approval.

## Guardrails

- Do not install torch, MMPose, MMCV, OpenCV, CUDA packages, or other large ML dependencies without explicit approval.
- Do not touch Blender's bundled Python for real inference dependencies.
- Do not claim real tracking until `test_data/green_field.mp4` pixels are actually processed.
- Do not claim in-Blender validation until `blender.exe` launches or a working Blender install is used.

## Cleanup State

Archived:
- `garbage/opencode-runtime-20260512-101539/`
- `garbage/markdown-consolidation-20260512/`
- `.codex/` is ignored; the canonical OpenCode skill lives in `.pm/skills/opencode-orchestrator/SKILL.md`.

Note:
- Git may show many deletions under `.pm/opencode-home/` because generated OpenCode runtime state was moved to `garbage/`. This is intentional cleanup, not data loss.

## Recommended Next Agent Action

Read:
1. `.pm/PM_HANDOFF.md`
2. `.pm/STATUS.md`
3. `.pm/work_items/WI-007.md`
4. `.pm/tasks/WI-007-A.md`
5. `docs/real_inference_setup.md`

Then produce `.pm/reports/WI-007-A-env-plan.md`.
