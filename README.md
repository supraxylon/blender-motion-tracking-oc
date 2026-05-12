# Blender Motion Tracking Enhancement

Build a Blender motion-tracking add-on around modern pose tracking.

Current direction:
- Primary backend: MMPose / RTMPose.
- v1 architecture: external inference worker -> cached JSON -> Blender import.
- Blender output first: empties and 2D pose tracks.
- Later: armature retargeting, SAM 2 / ByteTrack object tracking, optional WHAM 3D lift.

Start here:
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - combined project summary.
- [PLAN.md](PLAN.md) - full 18-week roadmap.
- [.pm/work_items/WI-002.md](.pm/work_items/WI-002.md) - next work item.
- [papers/README.md](papers/README.md) - research index.

Important notes:
- Do not embed PyTorch/MMPose inside Blender.
- Do not make this a general Python package repo.
- Keep heavy ML deps in an external worker environment.
- Use cached JSON as the first interface between tracking and Blender.
- LoRATv2 is useful research, but not the v1 backend because it outputs boxes, not pose keypoints.
