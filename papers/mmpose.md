# MMPose / RTMPose: Real-Time Human Pose Estimation and Tracking

**Authors:** OpenMMLab community (Tomtom et al.)  
**Venue:** RT-Moore paper, 2022; ongoing MMPose releases (35+ released)  
**Code:** https://github.com/open-mmlab/mmpose  
**License:** Apache-2.0

## Core Method
MMPose is a modular framework for human pose estimation containing multiple model families. The key models for Blender integration are:

**RTMPose (Real-Time Multi-Person Pose Estimation):** Uses RT-Transformer backbone with motion-aware temporal modeling. Single-stage detection + pose estimation pipeline running in real-time.

**RTMO (Real-Time Multi-Object pose):** One-stage multi-person pose tracker, designed for crowded scenes without separate detection + pose stages.

MMPose's inferencer accepts images, videos, image folders, or webcam streams and outputs structured keypoints with optional track IDs.

## Key Innovation
RTMPose achieves 75.8 AP on COCO keypoint detection at **90+ FPS on CPU** (i7-11700) and **430+ FPS on GPU** (GTX 1660 Ti). The framework supports full ONNX/TensorRT export, making it deployable outside of PyTorch. The tracker IDs from RTMO provide stable multi-person identity across frames — critical for Blender where you need consistent rig mappings.

## Relevance to Blender
HIGH. Produces 2D keypoints (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles) directly mappable to:
- **Empties** at each joint position (for motion paths)
- **Armature bones** (for direct retargeting to rigs)
- **Animation curves** (for recording motion over time)
- **Skeleton overlays** (for visual reference during video editing)

Apache-2.0 license, 7.6k stars, mature with 35+ releases. Official inferencer already handles video-to-JSON export.
