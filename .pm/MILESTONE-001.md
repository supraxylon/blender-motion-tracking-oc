# Milestone 001 - Cached Pose JSON to Blender Empties

Goal: build the first useful feature without heavy ML installs.

Feature flow:
1. Read cached pose JSON.
2. Validate the JSON contract.
3. Import it in Blender.
4. Create empties and keyframes for COCO 17 keypoints.

Main deliverables:
- Tracking JSON schema, sample cache, and validator.
- Blender add-on skeleton with JSON import operator.
- Smoke validation and short usage docs.

Local Blender is available under `blender/`. Use it for reference or headless validation if cheap. Do not edit Blender source in this milestone.

Do not install MMPose yet. Do not build armature retargeting yet.
