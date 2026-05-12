# Research Index

## Use First
| File | Summary |
| --- | --- |
| `mmpose.md` | Primary backend. RTMPose/RTMO gives 2D keypoints and track IDs. Best fit for Blender animation. |
| `rtmo.md` | Multi-person pose tracking from the MMPose family. Use for crowded scenes. |

## Use Later
| File | Summary |
| --- | --- |
| `sam2.md` | Promptable video masks. Good for roto, props, and person/object masks. |
| `bytetrack.md` | Practical box-based multi-object tracking. Useful for props and non-human objects. |
| `wham.md` | World-space 3D human motion. Powerful but blocked by SMPL/licensing and SLAM complexity. |

## Backup / Research Context
| File | Summary |
| --- | --- |
| `lorat.md` | Strong single-object box tracker. Useful for camera/object tracking, not v1 pose tracking. |
| `vasttrack.md` | Foundation-feature object tracking. Long-term category-general tracking idea. |
| `tracking-meets-lora.md` | LoRA adaptation for large tracking models. Useful if training/adaptation becomes needed. |
| `swintrack.md` | One-stream transformer tracking foundation. |
| `ostack.md` | Another single-stream transformer tracker. |
| `context-track.md` | Temporal context for occlusion and ambiguity. |
| `prack.md` | Motion primitive tracking for drift correction. |
| `promotion.md` | Motion prototypes relevant to camera-motion solving. |
| `planartrack.md` | Homography/planar tracking, useful for flat surfaces. |
| `damo.md` | Multi-scale tracking context. |
| `dasiamrpn.md` | Historical Siamese/RPN tracker context. |

## Bottom Line
Build v1 around MMPose/RTMPose. Keep SAM 2, ByteTrack, WHAM, and LoRATv2 as later adapters, not first implementation targets.
