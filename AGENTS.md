# AGENTS.md - Blender Motion Tracking Enhancement

## Current Direction
- Primary v1 backend: MMPose / RTMPose.
- Architecture: external inference worker -> cached JSON -> Blender import.
- First Blender output: pose/keypoint empties and overlays.
- Later outputs: armature retargeting, animation curves, SAM 2 masks, ByteTrack MOT, optional WHAM 3D lift.
- LoRATv2 is backup research for box/camera/object tracking, not the v1 pose backend.

## Rules
- Follow the current task file exactly.
- If acting as PM/orchestrator, read `.pm/PM_HANDOFF.md` before planning or delegation.
- If interacting with OpenCode, read `.pm/skills/opencode-orchestrator/SKILL.md`.
- Treat `docs/PROJECT_VISION.md`, `PLAN.md`, `documentation/PLAN.md`, `deep-research-report.md`, and `.pm/PLAN_SUMMARY.md` as planning context.
- Do not expand scope.
- Keep diffs small.
- Do not add large dependencies unless the task explicitly says to.
- Do not commit secrets.
- Always report commands and validation.

## Repo State
- This now has an MVP scaffold: cached JSON schema, external worker fixture, preview tool, and Blender add-on skeleton.
- No build/test/lint commands exist yet.
- `.pm/` holds PM state, tasks, work items, and OpenCode reports.

## OpenCode
- Server: `http://localhost:4096`
- Use `opencode run --attach http://localhost:4096 --session ses_1e5bc0f9dffeg2J57Yu13nCMhc ...`
- Do not use `opencode attach` for delegation; it opens the TUI.

## Garbage Collection
- Never delete files directly.
- If something should be removed, move it to `garbage/`.

## Where Work Goes
- Planning summaries: root docs or `.pm/`.
- Research notes: `papers/`.
- Future implementation: likely `src/` or a Blender add-on package, depending on the task.
