# Technical Planning Summary — Blender Motion Tracking

**Generated from:** `documentation/PLAN.md` + `deep-research-report.md`
**Date:** May 2026

---

## Core Project Goal

Integrate state-of-the-art human pose tracking into Blender's Video Editor for automatic camera rigging, motion retargeting, and animation. The system takes video input, produces 2D pose tracks with persistent IDs, maps them to Blender empties or armature bones, and optionally lifts to 3D.

---

## Recommended SOTA Tracking Backend

**MMPose / RTMPose** is the recommended primary backend for v1.

| Metric | Value |
|---|---|
| COCO AP (RTMPose-m) | 75.8 |
| CPU throughput | 90+ FPS (i7-11700) |
| GPU throughput | 430+ FPS (GTX 1660 Ti) |
| License | Apache-2.0 |
| Keypoints | 17 standard COCO body joints per person |

**Justification:** MMPose produces 2D keypoints directly mappable to Blender bones/empties. LoRATv2 outputs bounding boxes, which are not animation-ready. MMPose's real-time performance, permissive license, and成熟的 ecosystem make it the best v1 fit.

**Phase-two backends:** SAM 2 (promptable object masks), ByteTrack (general MOT), RTMO (multi-person).

---

## Proposed Blender Integration Architecture

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

**Key design decision:** All inference runs **out of process**. Blender spawns a Python subprocess with its own PyTorch environment. Communication is via cached JSON files, not embedded libraries.

---

## Key Constraints

1. **Not a Python project** — deliverable is a Blender add-on, not a standalone Python repo.
2. **Out-of-process inference** — PyTorch/CUDA must run in a separate process from Blender's bundled Python.
3. **JSON-first communication** — frame-to-frame data exchange via cached JSON files.
4. **Monocular 3D ambiguity** — 3D pose lifting is optional; depth recovery from a single camera is inherently ambiguous.
5. **SMPL licensing** — WHAM requires SMPL/SMPLify registration, adding complexity for 3D phase.
6. **Identity consistency** — crowded scenes require robust MOT to prevent ID swaps.

---

## Major Phases

| Phase | Weeks | Objective | Key Deliverable |
|---|---|---|---|
| **1** | 1-4 | MMPose integration | Blender add-on: video → MMPose → empties with keypoints + IDs |
| **2** | 5-8 | Armature retargeting | Skeleton bone mapping (17 joints → rig), automatic armature generation |
| **3** | 9-12 | Multi-person + objects | SAM 2, RTMO, ByteTrack integration for crowded scenes |
| **4** | 13-15 | 3D pose lifting | Optional WHAM-based 2D→3D lift, world-space positioning |
| **5** | 16-18 | Optimization & polish | <50ms latency, TensorRT, UI polish, documentation |

---

## Highest-Risk Assumptions

1. **MMPose keypoints map cleanly to common Blender rigs** (Humanoid, Rigify, Mixamo). Gaps exist for spine/neck/jaw/fingers beyond 17 COCO joints — mitigation: interpolation + user-defined bone mapping.
2. **Out-of-process JSON communication is fast enough** for practical workflows. Mitigation: optimize caching, profile end-to-end latency in Phase 5.
3. **Monocular 3D lifting produces usable results** without manual correction. Mitigation: keep 3D optional, offer manual correction tools.
4. **Multi-person ID stability** holds in real-world crowded footage. Mitigation: RTMO one-stage pipeline + ByteTrack fallback + visual ID labels.

---

## Immediate Next Steps

1. Set up Python environment with MMPose, RTMPose, RTMO, ONNX export.
2. Build external MMPose worker (subprocess from Blender Python).
3. Implement video-to-JSON inference pipeline.
4. Create Blender add-on panel (video input, person selection, output mode).
5. Map MMPose keypoints to Blender empties at joint positions.

---

## Contradictions, Gaps, and Unresolved Decisions

### Contradiction: Original LoRATv2 vs. Current MMPose Plan

The repo's AGENTS.md and initial PLAN_SUMMARY referenced **LoRATv2 + PrTrack + ProMotion** as the target architecture. The deep research and updated PLAN.md have **retconned to MMPose/RTMPose** as the primary backend. This is documented in PLAN.md section "Why MMPose / RTMPose (Not LoRATv2)?": LoRATv2 outputs bounding boxes, not pose keypoints suitable for animation. **Resolution:** MMPose is now the official direction; LoRATv2 is deprecated for v1 (backup for camera solving only).

### Gaps

1. **No Blender version target specified** — add-on API compatibility varies by Blender version. Decision needed.
2. **No hardware requirements defined** — GPU inference needs CUDA-capable hardware; CPU-only targets need RTMPose quantization strategy.
3. **No distribution model** — is this an open-source Blender marketplace add-on, Gumroad paid, or free GitHub release?
4. **No timeline for Phase 2-5** — only Phase 1 (weeks 1-4) has a concrete start date.

### Unresolved Decisions

1. **RTMPose vs. RTMO for v1** — RTMPose-m has higher accuracy; RTMO is faster for multi-person. Default not specified.
2. **Empty vs. Armature as v1 output** — PLAN.md lists both but Phase 1 deliverable emphasizes empties; armature retargeting is Phase 2. Unclear if v1 should include basic armature mapping.
3. **SMPL licensing path** — WHAM requires SMPL registration. Is there a legal/compliance path for this?
4. **3D lifting: WHAM vs. alternative** — WHAM is strongest but licensing-dependent. Alternatives like VideoPose3D not evaluated.
