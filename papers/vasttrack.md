# VastTrack: Vast Category Visual Object Tracking

**Authors:** Peng, Liming; Gao, Xiang; Liu, Xing; Li, Weize; Dong, Shichao; Zhang, Zechao; Fan, Haibin; and Zhang, Liangjian  
**Venue:** NeurIPS 2024  
**Code:** https://github.com/SJTU-ViSYS/VastTrack

## Core Method
VastTrack leverages vision foundation models (specifically DINOv2 features) for category-agnostic video object tracking. It treats tracking as a semantic feature matching problem, using pre-trained image features as the tracking signal rather than learned tracking-specific features. The framework extracts rich, general-purpose features from foundation models that capture object semantics, geometry, and texture simultaneously. A tracking-specific adapter head maps foundation features to target bounding boxes.

## Key Innovation
First framework to successfully use foundation model features (trained on millions of images) as the sole tracking signal without any tracking-specific pre-training. The key insight is that foundation model features are more transferable and diverse than tracking-specific features, enabling tracking of a vast category space (1000+ categories) from a single unified model. This eliminates the need to train separate trackers for different object types.

## Relevance to Blender Motion Tracking
High relevance for long-term motion tracking in Blender. Foundation model features handle dramatic appearance changes, illumination variations, and partial occlusions far better than traditional Siamese trackers. The category-agnostic nature means Blender's motion tracker could track ANY feature in the scene without pre-specifying the object type. However, the computational cost of DINOv2 inference may require optimization for Blender's real-time viewport.
