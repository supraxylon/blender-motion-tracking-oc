# Architecture Decision Log

**Source-plan context:** `.pm/PLAN_SUMMARY.md`, `documentation/PLAN.md`, `deep-research-report.md`

---

## ADR-1: Out-of-Process Inference

**Decision:** All ML inference (MMPose, SAM 2, ByteTrack, WHAM) runs as separate Python subprocesses outside Blender's embedded Python.

**Rationale:** Blender ships its own Python distribution. Embedding PyTorch/CUDA inside Blender's environment is complex and fragile. A separate process avoids DLL conflicts, simplifies dependency management, and lets Blender remain stable even if the inference worker crashes.

**Consequences:**
- Communication must use IPC (cached JSON files are the default).
- The MMPose worker requires its own Python environment with PyTorch installed.
- Slightly higher latency for large data transfer, justified by the decoupling benefit.

**Status:** **Accepted** — mandated by all three planning sources.

---

## ADR-2: JSON-First Communication

**Decision:** Data exchange between the MMPose worker and Blender uses cached JSON files, not in-memory pipes or shared libraries.

**Rationale:** JSON files provide a durable, inspectable, and debuggable exchange format. They decouple the inference pipeline from the Blender UI thread. This enables offline processing and re-running steps without re-tracking raw video.

**Consequences:**
- Requires a defined tracking result schema (BACKLOG item 2.3).
- File I/O becomes a performance factor — profiled in Phase 9.
- Parallel workers require unique file paths or lock mechanisms.

**Status:** **Accepted** — mandated by all three planning sources.

---

## ADR-3: MMPose/RTMPose as Primary Backend

**Decision:** MMPose (RTMPose family) is the primary pose estimation backend. SAM 2 and ByteTrack are phase-two additions. LoRATv2 is deprecated for v1.

**Rationale:** LoRATv2 outputs bounding boxes, not pose keypoints. Blender users need skeleton tracking for animation, camera rigging, and retargeting. MMPose provides 17 standard COCO keypoints per person with real-time performance (90+ FPS CPU, 430+ FPS GPU).

**Consequences:**
- Only 17 body joints are tracked in v1 — spine/neck/jaw/finger bones are interpolated.
- SAM 2/ByteTrack integration is deferred to phase M6.
- LoRATv2 may be retained as a camera-solving fallback (bounding boxes for tracking reference).

**Status:** **Accepted** — resolution documented in PLAN_SUMMARY contradiction section.

---

## ADR-4: Empties as v1 Output

**Decision:** Phase 1 output is Blender empties at keypoint positions. Armature retargeting is deferred to phase M5.

**Rationale:** The source plan explicitly lists armature retargeting as Phase 2 (weeks 5–8). Starting with empties provides immediate value (motion paths, visualization) without the complexity of skeleton mapping.

**Consequences:**
- Users get pose tracks → empties with motion paths in v1.
- Full animation pipeline requires Phase 2 delivery.
- The choice of empty vs. armature for v1 is intentional ambiguity (see Unresolved Decisions below).

**Status:** **Accepted** — aligns with phased plan in documentation/PLAN.md.

---

## Unresolved Decisions

### RTMPose-m vs. RTMO for v1
RTMPose-m has higher COCO AP (75.8); RTMO is faster for multi-person. The source plans do not resolve this. Recommendation: try both during M1 benchmarking (backlog item 1.2).

### Blender version target
No Blender version is specified in any source plan. Add-on API compatibility (e.g., `bpy.types.Panel` changes between 3.x and 4.x) is a decision that must be made.

### Hardware requirements
No GPU/CPU requirements are defined. GPU inference needs CUDA-capable hardware; CPU-only targets need RTMPose quantization strategy.

### Distribution model
Open-source marketplace add-on vs. paid release is undefined. No source plan addresses this.

### SMPL licensing path
WHAM requires SMPL/SMPLify registration. It is unclear whether a legal/compliance path exists. If blocked, WHAM should be replaced with an alternative (e.g., VideoPose3D).
