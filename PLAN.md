# Blender Motion Tracking Enhancement — Long-Term Implementation Plan

**Goal:** Integrate state-of-the-art human pose tracking into Blender's Video Editor for automatic camera rigging, motion retargeting, and animation.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Core Architecture](#core-architecture)
3. [Phased Implementation Plan](#phased-implementation-plan)
4. [Technical Challenges & Mitigations](#technical-challenges--mitigations)
5. [Milestones & Deliverables](#milestones--deliverables)
6. [Future Extensions](#future-extensions)

---

## Project Overview

### Why MMPose / RTMPose (Not LoRATv2)?

The deep research assessment found that **LoRATv2 outputs bounding boxes**, which are not directly useful for Blender's primary workflows: camera rigging, mocap, and animation retargeting. Blender users need **pose/keypoint tracking** that maps to skeletons, bones, and empties.

**MMPose / RTMPose is recommended** because it produces 2D keypoints directly mapable to Blender, with real-time performance (90+ FPS CPU, 430+ FPS GPU), Apache-2.0 license, and mature ecosystem.

### Current State
Blender's motion tracker places 2D anchor points and follows them for camera solving. It lacks:
- Pose/skeleton tracking for animation
- Multi-person identity consistency
- Motion retargeting to armatures
- Automatic rigging

### Target State
A pose-tracking pipeline producing:
- Keyframes from 2D pose tracks
- Retargeted armature bones from skeletal data
- Empties at joint positions with motion paths
- Smoothed, gap-filled motion for animation

### Key Success Metrics
| Metric | Target |
|--------|--------|
| Real-time inference (MMPose) | 90+ FPS CPU (RTMPose) |
| Multi-person stable IDs | 100% ID consistency |
| Pose accuracy (AP on COCO) | 75.8+ (RTMPose-m) |
| Blender empty/retarget mapping | Automatic |
| Pose lifting (phase 2) | Optional 2D→3D |

---

## Core Architecture

```
Blender Motion Tracking Add-on (NEW)
├── Phase 1: MMPose / RTMPose (2D pose + track IDs)
├── Phase 2: SAM 2 + ByteTrack (object masks + MOT)
├── Phase 3: WHAM (world-space 3D pose lift)
├── MMPose Worker: External process (not embedded)
├── JSON Cache: Keypoints + IDs between frames
├── Temporal Smoothing: Gap fill + interpolation
├── Blender Output: Empties + Armature mapping
└── Optional: 3D pose lift → animation curves
```

```
Video/Still Images
    → Blender Add-on Panel (launch MMPose worker)
        → MMPose Inference (RTMPose/RTMO)
            → 2D Keypoints + Track IDs (JSON cache)
                → Temporal Smoothing + Gap Fill
                    → Blender Empties / Armature Bones
                        → Optional 3D Pose Lift (WHAM)
                            → Animation Curves in Scene
```

---

## Phased Implementation Plan

### Phase 1: MMPose Integration (Weeks 1-4)
**Objective:** Build Blender add-on that runs MMPose externally and maps 2D pose tracks to empties.

**Tasks:**
- [ ] Set up Python environment with MMPose, RTMPose, RTMO, ONNX export
- [ ] Build external MMPose worker (subprocess from Blender Python)
- [ ] Implement video-to-JSON inference pipeline (MMPose inferencer → cached JSON)
- [ ] Create Blender add-on panel: video input, person selection, output mode
- [ ] Map MMPose keypoints to Blender empties at joint positions
- [ ] Add track ID visualization in Blender viewport
- [ ] Implement basic temporal smoothing on empty positions between frames

**Deliverables:**
- Working Blender add-on that accepts video, runs MMPose, creates empties
- Keypoints at all 17 standard body joints per person
- Persistent track IDs across frames
- Basic motion path display in 3D viewport

---

### Phase 2: Armature Retargeting (Weeks 5-8)
**Objective:** Map pose tracks to Blender armature bones for animation retargeting.

**Tasks:**
- [ ] Implement skeleton bone mapping (MMPose 17 joints → Blender rig structure)
- [ ] Create automatic armature generation from pose tracks
- [ ] Add IK/FK retargeting options (user selects preferred rig type)
- [ ] Implement animation curve generation from pose keyframes
- [ ] Add gap-filling for occluded frames (interpolation/ML fill)
- [ ] Polish UI: retarget mode selector, bone mapping config
- [ ] Test on diverse body types and poses

**Deliverables:**
- Automatic armature retargeting pipeline
- Animation curves populated from pose tracks
- Gap-filled motion for 50+ frame occlusions
- Retarget UI matching Blender's standard animation workflow

---

### Phase 3: Multi-Person + Object Tracking (Weeks 9-12)
**Objective:** Add SAM 2 for object tracking and ByteTrack for MOT support.

**Tasks:**
- [ ] Integrate SAM 2: promptable object masks for props/subjects
- [ ] Integrate RTMO for multi-person tracking (crowded scenes)
- [ ] Add ByteTrack: general object MOT backend (for non-human objects)
- [ ] Implement SAM 2 + MMPose pipeline (SAM finds person, MMPose tracks pose)
- [ ] Add object mask overlays to Blender (for compositing/matte generation)
- [ ] Support empty + armature creation for multiple subjects simultaneously

**Deliverables:**
- Multi-person tracking with stable IDs
- SAM 2 promptable object tracking for props/subjects
- ByteTrack MOT support for general objects
- Automatic creation of N armatures in crowded scene

---

### Phase 4: 3D Pose Lifting (Weeks 13-15)
**Objective:** Add optional 2D→3D pose lifting using WHAM or similar.

**Tasks:**
- [ ] Evaluate WHAM for Blender integration (SMPL licensing check)
- [ ] Implement optional 3D pose lift from MMPose 2D keypoints
- [ ] Add camera-relative → world-space transform
- [ ] Test on challenging camera motions (fast pans, zooms)
- [ ] Add fallback to 2D-only when 3D fails

**Deliverables:**
- Optional 3D pose output alongside 2D tracks
- World-space positioning in Blender scene
- Working 3D armatures for motion capture

---

### Phase 5: Optimization & Polish (Weeks 16-18)
**Objective:** Achieve target performance, polish UI, documentation.

**Tasks:**
- [ ] Profile inference pipeline end-to-end (Blender → MMPose → Blender)
- [ ] Optimize JSON caching and communication between processes
- [ ] Add ONNX export of RTMPose for faster inference
- [ ] Add TensorRT backend for GPU optimization
- [ ] Polish Blender UI: tooltips, presets, keyboard shortcuts
- [ ] Testing: 50+ diverse video sequences
- [ ] Documentation, tutorials, demo reel

**Deliverables:**
- <50ms round-trip latency (video → Blender empties)
- Real-time playback during inference
- User-tested, polished add-on
- Documentation and video demos

---

## Technical Challenges & Mitigations

### Challenge 1: PyTorch/CUDA Packaging Around Blender
**Problem:** Blender ships its own Python; adding a separate PyTorch/CUDA stack is complex.
**Mitigation:** Run MMPose **out-of-process**. Blender spawns a Python subprocess with its own PyTorch environment. No embedding of PyTorch into Blender. Use JSON file caching for frame-to-frame communication.

### Challenge 2: Identity Consistency in Crowded Scenes
**Problem:** Multiple people moving past each other — IDs can swap.
**Mitigation:** RTMO handles identity in one-stage pipeline (reduces ID switches). Fallback to ByteTrack for general MOT. Add visual ID labels in Blender UI.

### Challenge 3: Camera-Relative vs World-Space 3D
**Problem:** Monocular 3D pose lifting has depth ambiguity.
**Mitigation:** Keep 3D lifting optional. Use SMPL parameters as a guide, not definitive truth. Offer manual correction tools in Blender. WHAM's world-space recovery handles this better but requires SLAM.

### Challenge 4: Pose to Armature Mapping Complexity
**Problem:** 17 standard keypoints don't fully map to production rigs (spine, neck, jaw, fingers).
**Mitigation:** Interpolate missing bones from nearby keypoints. Allow user-defined bone mapping. Provide presets for common rig types (Humanoid, Rigify, Mixamo).

---

## Milestones & Deliverables

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 4 | MMPose working | Pose tracks → empties in Blender |
| 8 | Armature retargeting | Automatic rig mapping + animation |
| 12 | Multi-subject | SAM 2 + RTMO + ByteTrack integrated |
| 15 | 3D lifting (optional) | World-space 3D pose output |
| 18 | Release ready | Polished addon, docs, demos |

---

## Future Extensions

1. **Automated Character Generation** — Generate character models from video silhouettes
2. **Facial Expression Tracking** — Integrate with facial pose estimation for animation
3. **Hand Pose Tracking** — Retarget to finger articulation for gesture animation
4. **Video-to-Animation Pipeline** — Full automated mocap from video → rig → keyframes
5. **Live Camera Feed** — Real-time pose tracking from webcam for live performance capture
6. **Motion Style Transfer** — Transfer motion style between characters using pose tracks

---

## Notes

- **Primary target is MMPose/RTMPose** — produces keypoints directly mappable to Blender arms/empties
- **LoRATv2 is a backup** for camera solving (bounding boxes, not animation-ready)
- **SAM 2 is phase-two** for promptable object masks/roto tracking
- **RTMO for multi-person** scenes (one-stage tracker + poses)
- **ByteTrack for general MOT** (non-human objects in crowded scenes)
- **WHAM for 3D lifting** (advanced, later phase — SMPL licensing considerations apply)
- All inference should run **out of process** — separate Python worker vs Blender's embedded Python

---

*This plan will be updated iteratively as development progresses.*
*Last updated: May 2026*
