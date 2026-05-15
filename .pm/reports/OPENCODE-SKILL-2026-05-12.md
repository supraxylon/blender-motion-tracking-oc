# OpenCode Skill Report - 2026-05-12

## Delivered

- `.pm/skills/opencode-orchestrator/SKILL.md`
- README link to the skill.
- AGENTS.md instruction to read the skill before OpenCode interaction.
- PM handoff link to the skill.
- Status and housekeeping updates.

## What The Skill Covers

- OpenCode server URL resolution.
- Reachability checks.
- Starting `opencode serve`.
- Non-interactive delegation with `opencode run --attach`.
- Session usage.
- Config workaround using `XDG_CONFIG_HOME`.
- Report capture under `.pm/reports/`.
- Deliverable verification.
- Correction prompts.
- Parallel delegation boundaries.
- PM state updates.
- Cleanup and hard-claims rules.

## Validation

Structural check passed:

```powershell
PASS: skill frontmatter and title present
```

The official `quick_validate.py` script could not run under Blender bundled Python because `yaml` is unavailable:

```text
ModuleNotFoundError: No module named 'yaml'
```

No project code was changed by this validation attempt.

## Note

A `.codex/skills/opencode-orchestrator/` scaffold was created by the skill initializer, but this sandbox denied subsequent writes to that path. The canonical repo-local skill is `.pm/skills/opencode-orchestrator/SKILL.md`. `.codex/` is ignored in `.gitignore`.
