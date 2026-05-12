# WHAM: World-Human Alignment and Motion recovery

**Authors:** (See official project)  
**Venue:** WHAM paper, 2023-2024  
**Code:** https://github.com/hongsy/WHAM  
**License:** MIT

## Core Method
WHAM recovers **world-grounded 3D human motion** from monocular video. Given a single video camera feed, it estimates:
1. SMPL body model parameters (pose + shape)
2. Camera pose (SLAM-dependent)
3. World-space 3D position of each frame's person

The pipeline uses SMPL/SMPLify for body registration and a dedicated SLAM module for camera recovery. Evaluated on 3DPW, RICH, and EMDB benchmarks.

## Key Innovation
First method to produce **world-space** 3D poses (not just camera-relative). This matters for Blender because it means the recovered motion can be placed accurately in a Blender scene — the character's position relative to the environment is preserved, not just relative to the camera.

## Relevance to Blender
**Phase-three / future** integration target. WHAM is the strongest open option for **"video to mocap"** — taking video footage and producing 3D skeletal animation. However:
- Requires SMPL licensing/registration (legal friction)
- SLAM-dependent (unreliable with poor camera motion)
- Hard runtime profile (not clearly specified in docs)
- High engineering effort for Blender integration: retargeting from SMPL to production rigs is non-trivial

WHAM is the right target for a "video-to-mocap" Blender module, but only after the 2D pose tracking (MMPose) base is stable. Start with 2D → build → add 3D later.
