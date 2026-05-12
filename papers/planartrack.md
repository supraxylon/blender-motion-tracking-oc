# PlanarTrack: A Large-scale Challenging Benchmark for Planar Object Tracking

**Authors:** Liu, Xing; Liu, Xinyue; Yi, Zehui; Zhou, Xiang; Le, Tien; Zhang, Liangjian; Huang, Yong; Yang, Qiang; and Fan, Haibin  
**Venue:** ICCV 2023  
**Data:** https://planning.github.io/PlanarTrack/

## Core Method
PlanarTrack is a benchmark and associated method for tracking planar (flat) objects in videos — including billboards, screens, posters, and documents. The method uses homography estimation to track the full planar surface rather than just a bounding box, computing the 8-parameter homography matrix that relates the object between frames.

## Key Innovation
First large-scale benchmark specifically for planar object tracking with real-world challenging sequences featuring perspective changes, rotation, and non-rigid deformations. The associated tracker uses structure-aware feature extraction that preserves geometric relationships on the planar surface.

## Relevance to Blender Motion Tracking
MODERATE relevance for Blender. The homography-based tracking approach is relevant for motion tracking of planar surfaces in video (e.g., tracking a poster being placed on a wall in a shot). The homography matrix computation is related to Blender's camera solver which also deals with geometric transformations.
