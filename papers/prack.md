# PrTrack: Primitive-aware Tracker

**Authors:** (To be confirmed from source)  
**Venue:** CVPR 2024  

## Core Method
PrTrack introduces motion primitives as a complement to appearance-based tracking. The method models object motion as a combination of learned motion primitives (rigid translation, rotation, scaling, and affine transforms) with learned weights. At each frame, the tracker predicts motion primitive weights that guide the search region, combined with appearance features for target verification. Motion primitives serve as a strong prior that constrains the search space.

## Key Innovation
The key contribution is separating motion prediction from appearance verification. Traditional trackers only use appearance (template matching) which causes drift when targets change appearance. PrTrack adds a motion model built from learned primitives, giving it predictability similar to Kalman filters but learned from data. This reduces drift significantly in long sequences where appearance features become unreliable.

## Relevance to Blender Motion Tracking
Directly applicable. Blender's motion tracking problem (tracking 2D anchor points) is exactly the kind of problem where motion priors help. The "drift correction" problem Blender tracks face would be significantly reduced by PrTrack's motion primitive prediction. The method's combination of predicted motion + appearance verification maps cleanly to Blender's anchor point workflow.
