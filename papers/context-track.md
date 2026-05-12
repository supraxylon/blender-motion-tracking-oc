# Context-Guided Spatio-Temporal Video Grounding

**Authors:** Gu, Xing; Fan, Haibin*; Huang, Yong; Luo, Tao; and Zhang, Liangjian (*equal senior authoring)  
**Venue:** CVPR 2024  
**Code:** https://github.com/XingguangGu/ContextTrack

## Core Method
Context-Guided Spatio-Temporal Video Grounding learns to localize a target object in a video using both spatial features and temporal context. The method uses a context-guided module that aggregates temporal information across multiple frames to provide robust feature representations. This temporal context helps disambiguate targets that may look similar in individual frames but have distinguishable motion patterns over time.

## Key Innovation
The temporal context aggregation module that explicitly models long-range temporal dependencies. Unlike standard trackers that look at template + current frame pairs, this method leverages a history of previous frames to inform the current tracking decision, significantly improving robustness to occlusion and appearance ambiguity.

## Relevance to Blender Motion Tracking
MODERATE-HIGH relevance. The temporal context mechanism applies directly to Blender's need to track features across long video sequences. When a tracked feature point is temporarily occluded (e.g., passes behind another object), using context from previous frames helps maintain the track rather than losing the anchor point.
