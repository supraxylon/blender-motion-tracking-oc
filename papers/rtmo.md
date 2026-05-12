# RTMO: Real-Time Multi-Object Pose Tracking

**Authors:** OpenMMLab community  
**Venue:** MMPose framework release, ongoing  
**Code:** Part of MMPose repository (https://github.com/open-mmlab/mmpose)  
**License:** Apache-2.0

## Core Method
RTMO is MMPose's **one-stage multi-person pose tracking** model. Unlike traditional pipelines that run detection → pose estimation → tracking as separate stages, RTMO combines all three in a single network pass. Each predicted pose is assigned a persistent track ID across frames, enabling stable multi-person tracking without association post-processing.

## Key Innovation
Eliminates the detection + tracking pipeline by jointly predicting pose boxes and track IDs in one forward pass. This means:
- No identity-switching errors from separate tracking association
- Real-time performance (designed for crowded scenes)
- Clean API: input video → output keypoints with IDs

## Relevance to Blender
HIGH for **multi-person animation/mocap** workflows. In Blender, you might want to track multiple dancers, actors, or characters simultaneously. RTMO provides stable IDs per person, so you can map each tracked skeleton to a specific armature without manual ID management.

For single-person workflows, RTMPose (two-stage) is sufficient. RTMO is for multi-subject scenes.
