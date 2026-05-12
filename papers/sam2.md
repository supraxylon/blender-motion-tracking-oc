# SAM 2: Segmentation in Videos

**Authors:** Meta AI Research  
**Venue:** SAM 2 paper, 2024-2025  
**Code:** https://github.com/facebookresearch/sam2  
**License:** Apache-2.0 + BSD-3-Clause

## Core Method
SAM 2 extends the Segment Anything model to video by maintaining a memory bank of previously seen object masks and using a memory attention mechanism to propagate object segmentation across frames. Users provide point/click prompts on any frame, and SAM 2 propagates the mask through the entire video with consistent object identity.

**SAM 2.1 Large** reports 79.5 J&F on SA-V, 74.6 on MOSE, 80.6 on LVOS v2 at 39.5 FPS on A100. Supports multiple object prompts, mask propagation, and real-time inference on compatible hardware.

## Key Innovation
First video object segmentation model with true prompt-and-propagate UX — click once on any object in any frame, get consistent segmentation for that object across the entire video. Memory attention mechanism handles object appearance changes, occlusions, and temporary out-of-frame events.

## Relevance to Blender
BEST **phase-two** option for **promptable roto tracking** and **object mask tracking**. Useful for:
- Roto/sculpt tracking of arbitrary props/subjects in video
- Generating matte masks for compositing
- Tracking non-human objects (tools, vehicles, props)

Not suitable as primary motion tracking target — outputs masks, not keypoints or bone positions. However, SAM 2 masks can identify tracked regions for SAM 2 + MMPose hybrid workflows (SAM 2 finds the person, MMPose estimates their pose).
