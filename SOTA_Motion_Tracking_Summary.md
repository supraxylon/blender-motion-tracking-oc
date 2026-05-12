# Motion Tracking SOTA Research & Blender Integration — Updated Plan

**Prepared for:** Blender Motion Tracking System Redesign  
**Scope:** State-of-the-art pose/object tracking methods suitable for Blender's animation pipeline  
**Date:** May 2026 (Updated per deep research analysis)

---

## 1. WHY THE PRIMARY RECOMMENDATION CHANGED

### Initial Recommendation: LoRATv2 (bounding boxes)
LoRATv2 is excellent for single-object tracking with bounding box output. However, Blender users need **pose/keypoint data** for animation — not boxes. Bounding boxes don't map to armature bones, empties, or animation curves.

### Updated Recommendation: MMPose/RTMPose (keypoints)
MMPose produces 2D body keypoints directly mappable to Blender skeleton/empty/armature systems. This is the data Blender's animation pipeline needs — no intermediate conversion required.

---

## 2. UPDATED CANDIDATE COMPARISON (PER DEEP RESEARCH)

### Tier 1: Primary Targets for Blender

| Candidate | What it gives Blender | Blender Relevance | Integration Effort |
|------|------|----------|------|------|
| **MMPose / RTMPose** | 2D pose tracking with track IDs | **PRIMARY** — pose → empty/armature curves | **Medium** |
| **RTMO** | Multi-person one-stage tracker | **PRIMARY** — crowded scenes, stable IDs | **Medium** |
| **SAM 2** | Promptable object masks/roto | **Phase-2** — arbitrary object tracking | **Medium** |

### Tier 2: Strong Secondary Options

| Candidate | What it gives Blender | Blender Relevance | Integration Effort |
|------|------|----------|------|------|
| **ByteTrack** | Multi-object box tracking | **Phase-2** — general object MOT | **Medium** |
| **WHAM** | World-space 3D pose | **Phase-3** — video to mocap | **High** |
| **LoRATv2** | Single-object bounding boxes | **Camera solving only** (backup) | **Medium-High** |

### Tier 3: Historical Context

| Candidate | Venue | Relevance |
|------|---|-------|
| VastTrack | NeurIPS 2024 | Foundation model features (concept) |
| PrTrack | CVPR 2024 | Motion primitive drift correction |
| ProMotion | CVPR 2024 | Camera motion prototypes |
| SwinTrack | NeurIPS 2022 | One-stream transformer foundation |
| Context-Guided | CVPR 2024 | Temporal context for occlusion |
| OSTrack | ECCV 2022 | Single-stream tracking architecture |

---

## 3. RECOMMENDATION: MMPose/RTMPose + RTMO as Primary Integration Targets

**Choose:** MMPose / RTMPose (primary) + RTMO (multi-person)

### Why MMPose / RTMPose?

1. **Direct pose output.** 17 standard body keypoints (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles) map directly to Blender empties, armature bones, and animation curves.

2. **Real-time performance.** RTMPose-m achieves 75.8 AP on COCO at 90+ FPS CPU and 430+ FPS GPU. Fast enough for Blender's workflow without GPU dependency.

3. **Multi-person support.** RTMO (one-stage tracker) handles crowded scenes with stable track IDs — critical for tracking multiple characters/dancers simultaneously.

4. **Out-of-process architecture.** MMPose runs as a separate Python process, communicating via JSON cache files with Blender. No embedding of PyTorch into Blender.

5. **Open ecosystem.** Apache-2.0 license, 7.6k GitHub stars, 35+ releases, mature documentation, ONNX/TensorRT export pipeline.

6. **Extensible path.** SAM 2 for object masks, ByteTrack for MOT, WHAM for 3D lifting all build on this foundation.

### Integration Architecture

```
Phase 1: MMPose Pose Tracking
├── Video/still input → MMPose worker (external process)
├── RTMPose or RTMO inference (2D keypoints + track IDs)
├── JSON cache → mapped to Blender empties at joint positions
├── Temporal smoothing on empty positions between frames
└── Motion path visualization in 3D viewport

Phase 2: Armature Retargeting
├── MMPose keypoints → Blender armature bones (17-joint mapping)
├── Automatic armature generation from pose tracks
├── IK/FK retargeting options (Rigify, Mixamo presets)
└── Animation curves from pose keyframes

Phase 3: Multi-Subject + Object Tracking
├── SAM 2 for promptable object masks
├── RTMO for multi-person identity
├── ByteTrack for general MOT (props, vehicles, tools)
└── SAM 2 + MMPose pipeline (SAM finds person, MMPose tracks pose)

Phase 4: 3D Pose Lifting
├── Optional WHAM integration for world-space poses
├── SMPL body model registration
├── Camera pose estimation
└── 3D armature output for mocap
```

---

## 4. WHY NOT LORATV2?

LoRATv2 is excellent but outputs **bounding boxes**, which Blender's **animation pipeline** doesn't directly use:

| Concern | LoRATv2 | MMPose |
|---|---|---|
| Output format | Bounding box (4 values) | 17 keypoints (34 values) + IDs |
| Map to armature | No (needs intermediate 2D→pose step) | Yes (direct) |
| Map to empties | Only center point | Each joint = separate empty |
| Multi-person | Single object only | RTMO handles N people |
| Blender use case | Camera solving only | Rigging, mocap, animation, compositing |

If Blender adds a **camera solving** component to the tracker, LoRATv2 → SAM 2 pipeline becomes viable. For animation, MMPose is the natural choice.

---

## 5. EFFORT ESTIMATION

| Phase | Scope | Effort |
|-------|-------|--------|
| Phase 1: MMPose pose tracking | Video → keypoints → empties | **Medium** |
| Phase 2: Armature retargeting | Keypoints → bones + animation curves | **Medium** |
| Phase 3: Multi-subject tracking | SAM 2 + ByteTrack integration | **Medium** |
| Phase 4: 3D pose lifting | WHAM or similar 2D→3D | **High** |
| Phase 5: Optimization & polish | Performance, UI, docs | **Medium** |

**Total to production-ready Phase 1-2:** ~8 weeks
**Total for complete system with 3D:** ~18 weeks

---

*Full paper summaries available in `papers/` folder.*
*This assessment supersedes the initial LoRATv2 recommendation and the version in PLAN.md prior to deep research review.*
