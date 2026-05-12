# ByteTrack: Multi-Object Tracking by Low, High Confidence Association

**Authors:** Zeng et al.  
**Venue:** ECCV 2022 (original); still actively used and benchmarked  
**Code:** https://github.com/ifzhang/ByteTrack  
**License:** MIT

## Core Method
ByteTrack associates object detections across frames using a confidence-based association strategy. Unlike most trackers that discard low-confidence detections as false positives, ByteTrack **uses them** as well: high-confidence boxes are associated first, then low-confidence boxes handle occluded/truncated objects. This simple insight significantly improves MOT accuracy.

**MOT17 test:** 80.3 MOTA, 77.3 IDF1, 63.1 HOTA at ~30 FPS on V100.

## Key Innovation
The key insight: **don't throw away low-confidence detections**. Treat them as potential objects when high-confidence tracks are unavailable. This makes ByteTrack robust to occlusions and low-visibility situations — exactly the conditions Blender's motion tracker fails at.

Receives detector outputs in `(x1, y1, x2, y2, score)` format and emits MOT-format text results with persistent track IDs.

## Relevance to Blender
MODERATE — useful as a **multi-object box tracker backend**. ByteTrack could track any objects (not just humans) across frames, providing consistent IDs for Blender empties placed on tracked objects. However:
- Outputs bounding boxes, not keypoints
- Requires a separate object detector (not self-contained)
- Best as a phase-two option for general object tracking (props, cameras, vehicles)
- MIT license, straightforward PyTorch dependencies

For human animation/mocap use cases, MMPose/RTMPose is superior. For general object tracking, ByteTrack is the most practical open MOT backend.
