# Project Brief

Source docs:
- `PROJECT_SUMMARY.md`
- `PLAN.md`
- `documentation/PLAN.md`
- `deep-research-report.md`
- `.pm/PLAN_SUMMARY.md`

Goal: build a Blender add-on that turns video into animation-ready motion data.

Current v1 direction:
- MMPose / RTMPose first.
- Run inference outside Blender.
- Cache results as JSON.
- Import JSON into Blender.
- Create pose empties and overlays before armature retargeting.

Why external inference:
- Blender's bundled Python is fragile for PyTorch/CUDA.
- A worker crash should not crash Blender.
- JSON results are inspectable and reusable.

Near-term path:
1. Tracking JSON schema.
2. External MMPose worker CLI.
3. MMPose/RTMPose validation.
4. Blender add-on shell.
5. JSON import to empties.

Known risks:
- Large MMPose dependencies.
- RTMPose vs RTMO default not decided.
- Blender target version not pinned.
- COCO 17-keypoint output does not fully map to production rigs.
- WHAM/SMPL licensing blocks easy 3D lift.

Next work item: `.pm/work_items/WI-002.md`.
