# Milestone 002 - External Video-to-JSON Worker

Goal: create the first external worker path for `test_data/green_field.mp4`.

Deliverable target:
- A command-line worker that writes JSON matching `schemas/tracking_result.schema.json`.
- A probe report that says exactly what works and what blocks real MMPose inference.
- A validation path proving generated JSON can be consumed by the existing validator.

Strategy:
- First build a small worker scaffold with a fixture backend.
- Probe the local Python/MMPose/video environment separately.
- Only install heavy ML dependencies after the probe says it is safe and intentional.

Out of scope:
- Blender source edits.
- Armature retargeting.
- SAM2, ByteTrack, WHAM.
- Silent large dependency installs.

