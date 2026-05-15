# Project Vision

## Goal

Build a Blender motion tracking enhancement that turns video into useful animation data.
The v1 path is external pose inference, cached JSON, then Blender import/visualization.

## Current Direction

The active backend direction is RTMPose/MMPose for 2D human pose.
LoRATv2 remains useful research for box/object/camera tracking, but it is not the v1 pose backend because it does not produce animation-ready body keypoints.

## V1 Architecture

```text
video
-> external worker
-> RTMPose/MMPose pose inference
-> cached tracking JSON
-> Blender add-on import
-> keypoint empties / overlays
-> later armature retargeting
```

Heavy ML dependencies stay outside Blender. Blender's bundled Python remains focused on import, visualization, UI, and animation data creation.

## What Exists Now

- Cached tracking schema: `schemas/tracking_result.schema.json`.
- Sample cached data: `examples/sample_tracking_result.json`.
- JSON validator: `tools/validate_tracking_json.py`.
- Blender add-on scaffold: `src/blender_pose_tracker/`.
- External worker CLI: `tracking_worker.cli`.
- Working fixture backend: `--backend fixture`.
- Safe RTMPose placeholder: `--backend rtmpose` gives a clear missing-dependency error.
- SVG preview tool: `tools/render_tracking_preview.py`.
- Runtime probe: `tools/probe_blender_runtime.ps1`.

## What Works

- Fixture worker writes schema-compatible JSON.
- Generated JSON validates.
- Worker tests pass with Blender's bundled Python.
- Cached pose smoke test passes.
- SVG preview renders pose geometry from cached JSON.

## What Does Not Work Yet

- No real video-pixel pose inference has run.
- `test_data/green_field.mp4` is only used as a source path for fixture output.
- Repo-local `blender.exe` fails with a Windows side-by-side configuration error.
- `ffmpeg`, `ffprobe`, RTMPose, MMPose, torch, and OpenCV are not installed in the validated shell.

## Near-Term Milestones

1. Prepare real RTMPose/MMPose worker environment outside Blender.
2. Run real inference on `test_data/green_field.mp4`.
3. Validate and preview real tracking JSON.
4. Fix Blender launch or test inside a working Blender install.
5. Import real cached tracks into Blender as empties.

## Current PM Plan

Latest completed milestone:
- WI-006 / Milestone 003: real pose backend readiness.

Next work item:
- WI-007: first real RTMPose attempt.

First next task:
- WI-007-A: choose the external Python environment path and dependency install plan.

Guardrail:
- Do not install torch, MMPose, OpenCV, MMCV, or other large ML dependencies until the install plan is approved.

## Planning Sources

- `PLAN.md`
- `documentation/PLAN.md`
- `deep-research-report.md`
- `.pm/PLAN_SUMMARY.md`
- `.pm/BACKLOG.md`
