# Backlog

**Staged from:** `.pm/PLAN_SUMMARY.md`, `documentation/PLAN.md`, `deep-research-report.md`

---

## Execution Status - 2026-05-12

Completed:
- Cached JSON schema, sample data, and validator.
- Blender add-on skeleton for cached pose import.
- External worker CLI with fixture backend.
- MVP evaluation pack with SVG preview and runtime probe.
- Backend registry with safe `rtmpose` placeholder.
- Unified project vision and PM handoff docs.

Current next action:
- Run `WI-007-A`: choose the external Python environment path for real RTMPose/MMPose inference.

Do not install torch/MMPose/OpenCV until the user approves the WI-007-B install approach.

---

## Phase M1 — Research & Backend Selection (Weeks 1–2)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 1.1 | Set up Python environment with MMPose, RTMPose, RTMO                                     | Official install from OpenMMLab docs                     |
| 1.2 | Benchmark RTMPose-m vs RTMO on target hardware (CPU/GPU)                                | RTMO not yet evaluated per PLAN_SUMMARY                    |
| 1.3 | ONNX export validation for chosen model                                                    | Required for future optimization (Phase 5)                |

## Phase M2 — External Tracking Runner (Weeks 1–2, overlap)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 2.1 | Build MMPose worker (standalone Python script, CLI entrypoint)                          | Out-of-process by design per PLAN_SUMMARY                  |
| 2.2 | Implement video-to-JSON inference pipeline                                                | MMPose inferencer → cached JSON outputs                   |
| 2.3 | Establish tracking result schema                                                           | Must encode 2D keypoints + track IDs per person           |

## Phase M3 — Blender Add-on Skeleton (Weeks 2–3)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 3.1 | Create Blender add-on panel (video input, person selection, output mode)                 | Follows Blender developer conventions                      |
| 3.2 | Implement subprocess launcher (Blender Python → MMPose worker)                           | JSON-first communication via cached files                 |
| 3.3 | Implement JSON import from worker output                                                  | Frame-to-frame data exchange                              |

## Phase M4 — Visualization in Blender (Week 3)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 4.1 | Map MMPose keypoints to Blender empties at joint positions                                | 17 COCO body joints per person                            |
| 4.2 | Add track ID visualization in Blender viewport                                            | Persistent IDs across frames                              |
| 4.3 | Implement basic temporal smoothing on empty positions between frames                      | Gap fill + interpolation                                  |

## Phase M5 — Retargeting & Animation Mapping (Weeks 5–8)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 5.1 | Skeleton bone mapping (MMPose 17 joints → Blender armature)                              | Rigify, Humanoid, Mixamo presets                          |
| 5.2 | Automatic armature generation from pose tracks                                            | Phase 2 deliverable                                       |
| 5.3 | IK/FK retargeting options                                                                | User-selectable                                           |
| 5.4 | Animation curve generation from pose keyframes                                            | Populated from tracked motion                             |
| 5.5 | Gap-filling for occluded frames                                                          | Interpolation or ML fill (50+ frame occlusions)           |

## Phase M6 — Multi-Person + Object Tracking (Weeks 9–12)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 6.1 | Integrate SAM 2 for promptable object masks                                                | Phase 3 deliverable                                       |
| 6.2 | Integrate ByteTrack for general MOT                                                       | Non-human objects in crowded scenes                       |
| 6.3 | SAM 2 + MMPose composite pipeline                                                         | SAM finds person → MMPose tracks pose                     |
| 6.4 | Object mask overlays in Blender (compositing/roto)                                       |                                                         |

## Phase M7 — UI Workflow (Weeks 3–8, iterative)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 7.1 | Retarget mode selector + bone mapping config UI                                           |                                                         |
| 7.2 | Tooltips, presets, keyboard shortcuts                                                    | Phase 5 polish                                            |
| 7.3 | User workflow testing on diverse rigs                                                      |                                                         |

## Phase M8 — 3D Pose Lifting (Weeks 13–15, if licensing permits)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 8.1 | SMPL / WHAM licensing compliance check                                                    | Major blocker                                             |
| 8.2 | Optional 2D→3D pose lift from MMPose keypoints                                            | WHAM or alternative                                       |
| 8.3 | Camera-relative → world-space transform                                                   |                                                         |
| 8.4 | Fallback to 2D-only when 3D fails                                                         |                                                         |

## Phase M9 — Optimization & Polish (Weeks 16–18)

| #  | Item                                                                                     | Notes                                                    |
|----|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 9.1 | End-to-end profiling (Blender → MMPose → Blender)                                        |                                                         |
| 9.2 | ONNX export of RTMPose                                                                    | Faster inference                                          |
| 9.3 | TensorRT backend for GPU optimization                                                     |                                                         |
| 9.4 | Testing 50+ diverse video sequences                                                       |                                                         |
| 9.5 | Documentation, tutorials, demo reel                                                       |                                                         |

---

## Dependencies & Blockers

- Phase M6 (SAM 2, ByteTrack) depends on Phase M5 stabilizing first.
- Phase M8 (3D lifting) is blocked until SMPL licensing is resolved.
- Hardware requirements are undefined — no target GPU/CPU specification in source plans.
- Blender version target is unspecified — add-on API compatibility is an open decision.
