"""Deterministic fixture backend producing COCO-17 keypoints.

Output: 2 frames, 1 person, 17 keypoints, bbox, score, video_meta.
"""

from __future__ import annotations

from typing import Any

# Standing pose, normalized [0,1], 17 COCO joints.
_BASE: list[tuple[float, float, float]] = [
    (0.50, 0.06, 0.99),
    (0.47, 0.04, 0.97),
    (0.53, 0.04, 0.98),
    (0.45, 0.07, 0.92),
    (0.55, 0.07, 0.93),
    (0.42, 0.20, 0.98),
    (0.58, 0.20, 0.98),
    (0.40, 0.34, 0.96),
    (0.60, 0.34, 0.96),
    (0.38, 0.46, 0.93),
    (0.62, 0.46, 0.93),
    (0.46, 0.53, 0.99),
    (0.54, 0.53, 0.99),
    (0.47, 0.68, 0.95),
    (0.53, 0.68, 0.95),
    (0.48, 0.84, 0.91),
    (0.52, 0.84, 0.91),
]


def generate_fixture(
    source: str = "test_data/green_field.mp4",
    video_w: int = 1280,
    video_h: int = 720,
) -> dict[str, Any]:
    """Produce tracking result: 2 frames, 1 person, 17 keypoints, bbox, score."""
    persons: list[dict[str, Any]] = []
    for dx, dy in [(0.0, 0.0), (0.002, 0.003)]:
        keypoints = [
            {"x": min(max(x + dx, 0.0), 1.0), "y": min(max(y + dy, 0.0), 1.0), "score": s}
            for x, y, s in _BASE
        ]
        bx = min(max(0.36 + dx, 0.0), 1.0)
        by = min(max(0.04 + dy, 0.0), 1.0)
        bw = min(max(0.28, 0.0), 1.0 - bx)
        bh = min(max(0.82, 0.0), 1.0 - by)
        persons.append({
            "track_id": 0,
            "keypoints": keypoints,
            "score": 0.96,
            "bbox": {"x": bx, "y": by, "width": bw, "height": bh},
        })

    frames: list[dict[str, Any]] = [
        {"frame_index": i, "width": video_w, "height": video_h, "persons": [persons[i]]}
        for i in range(2)
    ]

    return {
        "video_meta": {
            "width": video_w,
            "height": video_h,
            "fps": 30.0,
            "duration": 2.0 / 30.0,
            "source": source,
        },
        "frames": frames,
    }
