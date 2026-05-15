# Blender Motion Tracking Enhancement

Build a Blender motion-tracking add-on around modern pose tracking.

Current direction:
- Primary backend: MMPose / RTMPose.
- v1 architecture: external inference worker -> cached JSON -> Blender import.
- Blender output first: empties and 2D pose tracks.
- Later: armature retargeting, SAM 2 / ByteTrack object tracking, optional WHAM 3D lift.

Start here:
- [docs/PROJECT_VISION.md](docs/PROJECT_VISION.md) - unified project vision and current state.
- [.pm/PM_HANDOFF.md](.pm/PM_HANDOFF.md) - PM handoff for future agents.
- [.pm/skills/opencode-orchestrator/SKILL.md](.pm/skills/opencode-orchestrator/SKILL.md) - OpenCode delegation skill.
- [PLAN.md](PLAN.md) - full 18-week roadmap.
- [docs/cached_pose_import.md](docs/cached_pose_import.md) - cached JSON import flow.
- [docs/external_worker.md](docs/external_worker.md) - external worker usage and fixture validation.
- [docs/mvp_evaluation.md](docs/mvp_evaluation.md) - current MVP evaluation commands and limits.
- [docs/real_inference_setup.md](docs/real_inference_setup.md) - next real RTMPose/MMPose setup path.
- [.pm/reports/WI-006-summary.md](.pm/reports/WI-006-summary.md) - latest milestone summary.
- [.pm/reports/HOUSEKEEPING-2026-05-12.md](.pm/reports/HOUSEKEEPING-2026-05-12.md) - latest housekeeping report.
- [.pm/reports/OPENCODE-SKILL-2026-05-12.md](.pm/reports/OPENCODE-SKILL-2026-05-12.md) - OpenCode skill creation report.
- [.pm/standups/2026-05-12.md](.pm/standups/2026-05-12.md) - latest stand-up.
- [.pm/work_items/WI-007.md](.pm/work_items/WI-007.md) - next work item.
- [papers/README.md](papers/README.md) - research index.

Important notes:
- Do not embed PyTorch/MMPose inside Blender.
- Do not make this a general Python package repo.
- Keep heavy ML deps in an external worker environment.
- Use cached JSON as the first interface between tracking and Blender.
- LoRATv2 is useful research, but not the v1 backend because it outputs boxes, not pose keypoints.
