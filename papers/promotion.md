# ProMotion: Prototypes As Motion Learners

**Authors:** Lu, Yuxuan; Liu, Di; Wang, Qiang; Han, Chi; Cui, Yuhui; Cao, Zhe; Zhang, Xiang; Chen, Yiran; and Fan, Haibin  
**Venue:** CVPR 2024  
**Code:** Available (see paper for link)

## Core Method
ProMotion learns motion representations using prototype-based learning rather than direct flow estimation. Instead of predicting per-pixel optical flow fields (as in RAFT or FlowFormer), ProMotion learns a set of motion prototypes from training data and represents each pixel's motion as a linear combination of these prototypes. The prototype weights are learned through a routing mechanism that assigns pixels to the most relevant prototype(s).

## Key Innovation
The key innovation is representing dense motion as a sparse combination of learned prototypes. This is more robust than direct flow prediction because prototypes capture common motion patterns (rigid body motion, rotation, perspective transforms) that naturally occur in camera movement. The prototype framework also makes the motion representation interpretable and efficient to compute.

## Relevance to Blender Motion Tracking
VERY HIGH relevance. Blender's camera tracking needs to estimate camera motion (rotation, translation, scaling) from feature point trajectories. Prototype-based motion learning directly captures the kind of rigid and perspective transforms that occur in camera movement. This approach would provide cleaner, more robust motion estimates for Blender's solver than dense optical flow methods.
