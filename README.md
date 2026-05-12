# Blender Motion Tracking Enhancement

**Integrating state-of-the-art human pose tracking (MMPose/RTMPose) into Blender for camera rigging, motion retargeting, and animation.**

---

## 🎯 Objective

Replace Blender's current template-based motion tracker with a modern AI-driven **pose tracking system** built on MMPose/RTMPose (OpenMMLab). This will provide:

- ✅ **Automatic armature retargeting** from video footage
- ✅ **Motion tracking for multiple characters** with stable IDs
- ✅ **2D → 3D pose lifting** for mocap workflows
- ✅ **Real-time performance** (90+ FPS CPU, 430+ FPS GPU)

---

## 📁 Project Structure

```
motion_tracking/
├── README.md              ← You are here
├── PLAN.md                ← Long-term roadmap
├── documentation/
│   └── PLAN.md
├── papers/                ← SOTA paper summaries
│   ├── mmpose.md          ← RTMPose/RTMO (PRIMARY)
│   ├── sam2.md            ← SAM 2 for object masks
│   ├── rtmo.md            ← Multi-person tracker
│   ├── bytetrack.md       ← MOT backend
│   ├── wham.md            ← World 3D pose lift
│   ├── lorat.md           ← Single-object tracker (backup)
│   ├── vasttrack.md       ← Foundation model tracking
│   ├── prack.md           ← Motion primitive drift correction
│   ├── promotion.md       ← Camera motion prototypes
│   ├── ostack.md          ← Single-stream transformer
│   ├── tracking-meets-lora.md
│   ├── context-track.md
│   ├── planartrack.md
│   ├── swintrack.md
│   ├── damo.md
│   └── dasiamrpn.md
└── src/                   ← Integration code (future)
```

---

## 🔬 Core Technology (Updated per Deep Research)

| Priority | Component | Source | Purpose |
|------|---|------|---|
| **#1** | **MMPose / RTMPose** | OpenMMLab | Primary pose tracker (2D keypoints + IDs) |
| **#2** | **RTMO** | MMPose | Multi-person tracking (crowded scenes) |
| **#3** | **SAM 2** | Meta AI | Promptable object masks for roto (phase 2) |
| **#4** | **ByteTrack** | ECCV 2022 | General MOT backend (props/objects) |
| **#5** | **WHAM** | Research | World-space 3D pose lift (phase 3) |
| **Backup** | **LoRATv2** | NeurIPS 2025 | Single-object bounding boxes (camera solving only) |

---

## 🚀 Why MMPose Over LoRATv2?

**Deep research identified a critical distinction:** Blender users need **animation-ready pose data**, not bounding boxes.

| | LoRATv2 | MMPose/RTMPose |
|--|---|--|
| **Output** | 2D bounding boxes | 17 body keypoints + track IDs |
| **Map to** | Camera tracking points | Armature bones, empties, curves |
| **Blender use** | Camera solving only | Rig retargeting, mocap, animation |
| **License** | Apache-2.0 | Apache-2.0 |
| **FPS** | 119 FPS | 90+ CPU, 430+ GPU |

MMPose directly produces the data Blender's animation pipeline needs — no intermediate conversion from boxes to poses.

---

## 📊 Key Metrics We'll Track

- **Inference Speed:** 90+ FPS CPU (target matches RTMPose baseline)
- **Pose Accuracy:** 75.8+ AP on COCO (matches RTMPose-m)
- **Identity Stability:** 100% track ID consistency in non-crowded scenes
- **Blender Mapping:** Automatic pose → armature/empty conversion
- **Latency:** <50ms round-trip (video input → Blender empty positions)

---

## 📝 Notes

- This project targets **human pose tracking and animation retargeting**, not just camera tracking.
- MMPose runs **out-of-process** — a separate Python worker, not embedded in Blender.
- Focus is on **2D pose estimation with persistent IDs**, plus optional 3D pose lifting.
- LoRATv2 and other SOT trackers are preserved for camera-solving work but are **not the primary target**.

---

*Last updated: May 2026*  
*Author: Blender Motion Tracking Enhancement Project*
