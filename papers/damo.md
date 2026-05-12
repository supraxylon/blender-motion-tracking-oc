# DAMO Tracker: Efficient Multi-Scale Tracking

**Authors:** Fan, Haibin; Liu, Xing; and Ling group collaborators  
**Venue:** Multiple iterations (ICCV 2019 foundational work, evolved through 2022-2025)  
**Code:** Available in related GitHub repositories

## Core Method
The DAMO (Detection and Action Monitoring Optimization) Tracker framework uses multi-scale feature learning for robust visual tracking. It extracts features at multiple scales from the search region and uses adaptive feature fusion to combine scale-specific information. The multi-scale approach handles target scale changes that occur when the camera zooms or the target moves toward/away from the camera.

## Key Innovation
The adaptive multi-scale feature fusion module that automatically learns which scales are most relevant at each timestep. Rather than using fixed multiple scales, DAMO learns a scale-aware weighting that emphasizes the most informative scales for the current tracking context.

## Relevance to Blender Motion Tracking
MODERATE-HIGH relevance. Multi-scale feature handling is important for Blender's motion tracker which needs to handle feature points at varying distances from the camera. As the camera moves, points at different depth levels scale at different rates, and the multi-scale approach helps maintain track accuracy across varying zoom levels.
