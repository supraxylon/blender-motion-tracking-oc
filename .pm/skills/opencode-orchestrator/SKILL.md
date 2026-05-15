---
name: opencode-orchestrator
description: Use when Codex needs to interact with OpenCode as a delegated implementation agent: starting or attaching to an OpenCode server, running non-interactive `opencode run --attach` tasks, passing task files and planning context, saving OpenCode reports, verifying deliverables, handling failed or blank OpenCode output, and maintaining PM state for this repository.
---

# OpenCode Orchestrator

## Role

Act as the PM/orchestrator. Use OpenCode for scoped implementation work, then verify the result yourself before claiming progress.

Do not use OpenCode as a black box. Treat it like a worker whose output must be checked.

## Read First

Before delegating, read:

1. `.pm/PM_HANDOFF.md`
2. `.pm/STATUS.md`
3. The active `.pm/work_items/*.md`
4. The active `.pm/tasks/*.md`
5. Relevant project docs, usually `docs/PROJECT_VISION.md` and `docs/real_inference_setup.md`

## Server URL

Resolve the OpenCode server URL in this order:

1. `$env:OPENCODE_SERVER_URL`
2. `.pm/opencode_server.txt`
3. `http://localhost:4096`

PowerShell:

```powershell
$server = $env:OPENCODE_SERVER_URL
if (-not $server -and (Test-Path .pm\opencode_server.txt)) {
  $server = (Get-Content -Raw .pm\opencode_server.txt).Trim()
}
if (-not $server) { $server = "http://localhost:4096" }
```

Known project server:

```text
http://localhost:4096
```

Known prior session:

```text
ses_1e5bc0f9dffeg2J57Yu13nCMhc
```

Use a session only if it is provided by the environment or current PM state.

## Config Workaround

If OpenCode fails with `EEXIST` or config-path errors, redirect config into `.pm` for that command:

```powershell
$env:XDG_CONFIG_HOME = (Resolve-Path '.pm').Path + '\opencode-config'
```

If OpenCode creates `.pm/opencode-home` or `.pm/opencode-config`, keep those out of active PM records. They may be moved to `garbage/`.

## Reachability Check

Use `opencode run --attach`, never `opencode attach`.

```powershell
opencode run --attach $server "Respond with exactly: OpenCode server is reachable."
```

If using a session:

```powershell
opencode run --attach $server --session $session "Respond with exactly: OpenCode server is reachable."
```

Blank stdout can still happen. If exit code is `0`, verify later task deliverables directly.

## Starting Server

Only start the server if it is not reachable and the user has indicated a server should run locally.

PowerShell:

```powershell
New-Item -ItemType Directory -Force .pm | Out-Null
Start-Process opencode -ArgumentList "serve --port 4096 --hostname 127.0.0.1" -RedirectStandardOutput ".pm/opencode-server.log" -RedirectStandardError ".pm/opencode-server.err.log" -WindowStyle Hidden
Set-Content .pm/opencode_server.txt "http://localhost:4096"
$env:OPENCODE_SERVER_URL = "http://localhost:4096"
```

Then wait briefly and run the reachability check again.

## Delegation Command Pattern

Keep tasks scoped. Attach the reusable delegation prompt, the task file, and only relevant context.

```powershell
$env:XDG_CONFIG_HOME = (Resolve-Path '.pm').Path + '\opencode-config'
opencode run `
  --attach $server `
  --file .pm\OPENCODE_DELEGATION_PROMPT.md `
  --file .pm\tasks\WI-007-A.md `
  --file .pm\PM_HANDOFF.md `
  --file docs\PROJECT_VISION.md `
  --file docs\real_inference_setup.md `
  --format json `
  "Implement only .pm/tasks/WI-007-A.md. Keep scope small. Do not install dependencies. Return files changed, commands run, validation, blockers, and next task." `
  *> .pm\reports\WI-007-A-opencode.txt
```

If a session is required, add:

```powershell
--session $session
```

## Prompt Rules

Tell OpenCode:

- Implement only the attached task.
- Do not expand scope.
- Do not make unrelated edits.
- Do not install heavy dependencies unless the task explicitly says to and approval exists.
- Keep diffs small.
- Run validation or explain why validation cannot run.
- Return files changed, commands run, validation, blockers, and next task.

For PM/planning tasks, prefer direct language:

```text
Read the attached files. Produce the requested report. Do not edit product code. Do not install anything.
```

For implementation tasks, include exact deliverables and acceptance checks from the task file.

## Report Capture

Always save raw OpenCode output under `.pm/reports/`.

Recommended pattern:

```powershell
... *> .pm\reports\<TASK-ID>-opencode.txt
```

If JSON output is reliable in the current environment:

```powershell
... --format json | Tee-Object -FilePath .pm\reports\<TASK-ID>-opencode.json
```

If stdout is blank but files changed, write your own verified summary:

```text
.pm/reports/<TASK-ID>-summary.md
```

## Verification After Every Task

Do not move on until deliverables exist or a blocker is documented.

For a task, check:

```powershell
Test-Path <expected-file>
```

Then inspect content:

```powershell
Get-Content -Raw <expected-file>
```

Then run validation commands from the task file.

Common validation commands:

```powershell
$py = Resolve-Path 'blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe'
& $py -S tests\smoke_validate_cached_pose.py
& $py -S tests\test_tracking_worker_fixture.py
& $py -S tools\validate_tracking_json.py outputs\green_field_tracking.json
```

## Failure Handling

If OpenCode fails or misses a deliverable:

1. Write `.pm/reports/<TASK-ID>-correction-prompt.md`.
2. State the exact missing deliverable or validation failure.
3. Send the correction prompt with `opencode run --attach`.
4. Save the correction output.
5. Verify again.

Do not silently skip failures.

## Parallel Work

Parallelize only independent tasks with separate write areas.

Good parallel split:
- Environment probe report.
- Documentation report.
- Isolated worker module.

Bad parallel split:
- Two agents editing the same CLI file.
- A docs agent summarizing code that another agent has not finished.

When parallel OpenCode output is blank, inspect deliverables directly and write verified summaries.

## PM Updates

After every meaningful task, update:

- `.pm/STATUS.md`
- `.pm/standups/YYYY-MM-DD.md`
- `.pm/reports/<TASK-ID>-summary.md`

When an architecture decision changes, update `.pm/DECISIONS.md`.

When the next task changes, update `.pm/BACKLOG.md` and `.pm/PM_HANDOFF.md`.

## Cleanup

Never delete directly.

Move removable clutter to:

```text
garbage/<clear-folder-name>/
```

Generated OpenCode runtime state belongs in `garbage/`, not active `.pm/`.

## Hard Claims Rule

Only claim:

- "OpenCode completed" after deliverables exist.
- "Validation passed" after you ran the command.
- "Real inference ran" after video pixels were processed by a real backend.
- "Blender validation passed" after `blender.exe` launches or a working Blender install runs the check.

Use "fixture" or "synthetic" for fixture backend outputs.
