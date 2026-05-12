# Project Summary

## Goal
Create a Blender add-on that turns video into usable animation data. The first useful version should run pose inference outside Blender, cache results as JSON, then import those tracks into Blender as empties and later armature animation.

## Decision
Use MMPose / RTMPose first. It produces 2D human keypoints that map directly to Blender joints, empties, bones, and animation curves.

LoRATv2 is no longer the primary v1 backend. It is a strong single-object tracker, but its output is bounding boxes. Boxes help camera/object tracking; they do not directly solve pose, mocap, or armature retargeting.

## Architecture
```text
Video
-> external MMPose worker
-> cached tracking JSON
-> Blender add-on import
-> empties / pose overlays
-> later armature retargeting
-> optional 3D lift
```

## Backend Tiers
| Tier | Backend | Use |
| --- | --- | --- |
| 1 | MMPose / RTMPose | Primary 2D pose tracking |
| 1 | RTMO | Crowded multi-person pose tracking |
| 2 | SAM 2 | Promptable masks and roto/object tracking |
| 2 | ByteTrack | General box-based MOT |
| 3 | WHAM | Optional world-space 3D human motion |
| Backup | LoRATv2 | Single-object boxes, camera/object tracking |

## Why External Inference
Blender ships its own Python. PyTorch/CUDA-heavy dependencies are fragile inside it. The add-on should launch an external worker and read JSON output. This keeps Blender stable, makes results inspectable, and lets users rerun Blender-side import/retargeting without rerunning inference.

## First Milestones
1. Define the tracking JSON schema.
2. Build an external MMPose worker CLI.
3. Validate RTMPose/RTMO on sample media.
4. Build Blender add-on skeleton.
5. Import JSON and create keypoint empties.
6. Add smoothing and track ID display.
7. Add armature retargeting.

## Risks
- MMPose environment setup may pull large dependencies.
- RTMPose vs RTMO default is unresolved.
- Blender target version should be pinned before add-on work.
- COCO 17-keypoint output does not fully describe production rigs.
- WHAM has SMPL licensing and SLAM complexity.

## Current Next Work
WI-002 is the next planned work item. It currently asks for MMPose validation, an external worker, and a JSON schema. Before running it, consider doing the JSON schema first to avoid premature large dependency installation.

## File Map
| File | Status |
| --- | --- |
| `PROJECT_SUMMARY.md` | Canonical short summary |
| `PLAN.md` | Full roadmap |
| `documentation/PLAN.md` | Duplicate of root `PLAN.md` kept for prompts/tools |
| `deep-research-report.md` | Detailed backend recommendation |
| `garbage/cleanup-2026-05-12/archived-root-notes/` | Archived raw/older root notes superseded by this summary |
| `garbage/cleanup-2026-05-12/pm-runtime-debug/` | Archived OpenCode runtime/debug noise |
| `papers/*.md` | Individual research notes |
| `.pm/*` | PM state, backlog, tasks, OpenCode reports |
