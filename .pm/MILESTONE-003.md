# Milestone 003 - Real Pose Backend Readiness

Status: complete.

Goal: prepare the external worker for real RTMPose/MMPose integration without installing heavy dependencies.

Delivered:
- Backend registry.
- Fixture backend adapter.
- RTMPose missing-dependency adapter.
- Real inference setup doc.
- Unified project vision doc.
- PM handoff and housekeeping docs.

Validation:
- Fixture worker still writes valid JSON.
- Fixture tests pass.
- RTMPose backend fails clearly when dependencies are missing.

Next:
- WI-007 should create or use an external Python environment and make the first real RTMPose/MMPose inference attempt on `test_data/green_field.mp4`.
- Start with WI-007-A; do not install heavy dependencies before approval.
