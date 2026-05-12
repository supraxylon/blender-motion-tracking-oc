# SwinTrack: A Simple and Strong Baseline for Transformer Tracking

**Authors:** Lin, Liang; Fan, Haibin*; Zhang, Zechao; Xu, Yu; and Ling, Haibin (*equal contribution)  
**Venue:** NeurIPS 2022  
**Code:** https://github.com/hengam/SwinTrack

## Core Method
SwinTrack is the first effective one-stream transformer architecture for video object tracking. It uses a Swin Transformer backbone for feature extraction and introduces a simple yet effective single-stream interaction module. Unlike two-stream trackers (SiamFC, SiamRPN) that process template and search frames separately then combine features, SwinTrack concatenates template and search features and processes them through shared transformer blocks.

## Key Innovation
Demonstrated that a single-stream transformer can match or beat two-stream Siamese trackers in accuracy. Proposed the first effective use of Swin Transformer (shifted window attention) for tracking, showing that hierarchical feature representations with shifted windows capture multi-scale object appearance better than traditional Siamese correlation layers.

## Relevance to Blender Motion Tracking
Foundational relevance. SwinTrack is the architectural predecessor to LoRAT and shows the viability of transformer-based tracking. For Blender, the Swin Transformer backbone provides a good template matching mechanism, and the shifted-window attention captures multi-scale features which is important for tracking points that change scale as camera zooms in/out.
