# WI-001-TASK-3 - First Implementation Work Item

## Task ID
WI-001-TASK-3

## Parent Work Item
WI-001

## Objective
Create the first implementation work item based on the aligned roadmap.

## Source-Plan References
- `.pm/PLAN_SUMMARY.md`
- `.pm/BACKLOG.md`
- `.pm/DECISIONS.md`
- `.pm/PROJECT_BRIEF.md`
- `documentation/PLAN.md`
- `deep-research-report.md`

## Context
WI-002 should be the earliest practical implementation step from the roadmap. It must be small enough for OpenCode to execute safely and must not attempt to build the whole system.

## Files Likely to Touch
- `.pm/work_items/WI-002.md`
- `.pm/STATUS.md` only if a blocker prevents delivery

## Requirements
- Base WI-002 on `.pm/PLAN_SUMMARY.md`, `.pm/BACKLOG.md`, and the source documents.
- WI-002 must contain exactly three implementation tasks.
- Each task must have a concrete deliverable.
- Each task must include acceptance criteria.
- Each task must define what is out of scope.
- Prefer the earliest practical implementation step from the roadmap.
- Include source-plan references.
- Avoid asking OpenCode to build the whole system.
- Avoid large dependency installation.

## Deliverable
`.pm/work_items/WI-002.md`

## Acceptance Criteria
- `.pm/work_items/WI-002.md` exists.
- WI-002 contains exactly three tasks.
- Each task has a concrete deliverable.
- Each task has acceptance criteria.
- Each task has out-of-scope boundaries.
- WI-002 is directly aligned with the master plan.

## Validation Steps
- Confirm `.pm/work_items/WI-002.md` exists.
- Count that WI-002 defines exactly three tasks.
- Check that all tasks have deliverables, acceptance criteria, and out-of-scope boundaries.
- Check that WI-002 is aligned with the source-plan-backed roadmap.

## Out of Scope
- Executing WI-002.
- Installing large dependencies.
- Building the full Blender integration.

## Final Report Required
Return a final report with:
- Files changed
- Commands run
- Tests or validation run
- Summary
- Blockers
- Suggested next task
