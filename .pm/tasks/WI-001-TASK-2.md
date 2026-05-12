# WI-001-TASK-2 - Backlog and Decision Log

## Task ID
WI-001-TASK-2

## Parent Work Item
WI-001

## Objective
Create a source-plan-aligned backlog and architecture decision log.

## Source-Plan References
- `.pm/PLAN_SUMMARY.md`
- `documentation/PLAN.md`
- `deep-research-report.md`

## Context
The project needs staged planning artifacts that translate the source documents into milestones without jumping into implementation. Preserve ambiguity where the plan has not resolved details.

## Files Likely to Touch
- `.pm/BACKLOG.md`
- `.pm/DECISIONS.md`
- `.pm/PROJECT_BRIEF.md`
- `.pm/STATUS.md` only if a blocker prevents delivery

## Requirements
- Use `.pm/PLAN_SUMMARY.md` as input.
- Create a staged backlog aligned with the master plan.
- Include milestones such as research/backend selection, external tracking runner, tracking result schema, Blender add-on skeleton, Blender JSON import, visualization in Blender, retargeting/animation mapping, UI workflow, packaging, and documentation if consistent with the sources.
- Add architecture decisions only where the plan supports them.
- Preserve uncertainty where the plan is ambiguous.
- Do not create implementation tasks yet beyond high-level backlog items.
- In `.pm/PROJECT_BRIEF.md`, explain why heavy ML inference should run outside Blender for v1 unless the source plans say otherwise.
- In `.pm/PROJECT_BRIEF.md`, explain why Blender should initially consume cached tracking outputs.
- Explicitly note that `.pm/PLAN_SUMMARY.md`, `documentation/PLAN.md`, and `deep-research-report.md` are planning sources.

## Deliverables
- `.pm/BACKLOG.md`
- `.pm/DECISIONS.md`
- `.pm/PROJECT_BRIEF.md`

## Acceptance Criteria
- `.pm/BACKLOG.md` exists and is staged into clear milestones.
- `.pm/DECISIONS.md` exists and contains at least one justified ADR or a note explaining why no ADR can be made yet.
- `.pm/PROJECT_BRIEF.md` exists and accurately summarizes the project.
- The backlog reflects the source documents instead of generic assumptions.

## Validation Steps
- Confirm all three deliverables exist.
- Check that backlog stages align with MMPose/RTMPose v1, JSON cache, Blender import/visualization, and later retargeting or 3D lifting as supported by the source documents.
- Check that any ADR is grounded in the source documents.

## Out of Scope
- Writing production code.
- Creating Blender files.
- Installing ML libraries.

## Final Report Required
Return a final report with:
- Files changed
- Commands run
- Tests or validation run
- Summary
- Blockers
- Suggested next task
