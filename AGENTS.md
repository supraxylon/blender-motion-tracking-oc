# AGENTS.md — Blender Motion Tracking Enhancement

## Repo State
No implementation code yet. This is a **research/plan repo** for a Blender motion tracking enhancement project. All code will be written from scratch.

## Project Goal
Integrate **LoRATv2** (NeurIPS 2025 Spotlight) into Blender's Video Editor motion tracker to replace the current template-based tracker. Target architecture uses LoRATv2 + PrTrack (drift correction) + ProMotion (camera solving).

## Key Constraint
This is **not a Python project**. The deliverable is a **Blender C++ add-on** (Pybind11) loading a **TorchScript/ONNX** model. Do not create Python project structure expecting pip/venv/pytest — those are for LoRATv2 baseline reproduction, not this repo.

## Structure
```
papers/          ← Research summaries (already written)
documentation/   ← PLAN.md (duplicated from root — consistent)
PLAN.md          ← 18-week phased roadmap (root)
README.md        ← Project overview
```

## OpenCode Config
- Location: `.opencode/opencode.json`
- Provider: Ollama local at `http://localhost:12434/engines/v1`
- Models: `qwen3.6:35b-a3b` (default), `gemma4:31b`, `qwen3.5:9b`, `deepseek-r1:8b`

## Before Working (What to Assume)
- No build/test/lint commands exist — none to run
- No `src/` directory — it's a planned addition
- LoRATv2 source is external (https://github.com/hengam/lorat) — you'd need to clone it to reproduce
- Blender add-on target follows https://developer.blender.org/ conventions

## Garbage Collection
- NEVER delete files directly. When something should be removed, move it to a `garbage/` folder instead. This prevents accidental data loss and makes it easy to recover.

## What to Produce
- Code should go in `src/` (not yet created)
- Paper notes live in `papers/` (already written)
- Progress updates in `PLAN.md` checklist items
