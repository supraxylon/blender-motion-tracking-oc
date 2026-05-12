# LoRAT / LoRATv2: Low-Rank Attention for Video Object Tracking

**Authors:** Lin, Liang; Fan, Haibin; Zhang, Zechao; Huang, Yong; Wang, Yaqing; Xu, Yu; and Ling, Haibin  
**Venue:** LoRAT: ECCV 2024; LoRATv2: NeurIPS 2025 (Spotlight)  
**Code:** https://github.com/hengam/lorat  
**License:** Apache-2.0

## Core Method
LoRAT replaces expensive cross-attention in one-stream trackers with low-rank temporal modeling. LoRATv2 adds adaptive rank selection and temporal feature compensation for improved accuracy. Outputs 2D bounding boxes for single objects per video.

**LoRATv2 L-224 variant:** 0.742 LaSOT SUC, 119 FPS inference speed (up from 52 FPS, ~2.3x faster).

## Key Innovation
Decouples temporal modeling from feature extraction using low-rank decomposition. Enables tracking with large foundation model backbones at low compute cost.

## Relevance to Blender
**Secondary backup** for camera solving workflows. LoRATv2 is excellent for single-object tracking and is the strongest recent SOT engine from Heng Fan's research group. However, it outputs **bounding boxes only** — not keypoints or skeleton data. Bounding boxes are not directly useful for Blender's primary workflow (animation/mocap rig retargeting).

Use LoRATv2 + SAM 2 pipeline for camera solving if Blender's Video Editor tracker is replaced. Not the right choice for phase-one pose tracking.
