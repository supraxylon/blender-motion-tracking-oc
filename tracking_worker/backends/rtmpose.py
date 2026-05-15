"""RTMPose backend placeholder.

This module intentionally avoids importing heavy ML packages at import time.
The real implementation belongs in the external worker environment, not in
Blender's Python runtime.
"""

from __future__ import annotations

from importlib.util import find_spec
from typing import Any

from tracking_worker.backends.registry import BackendUnavailableError


REQUIRED_MODULES = {
    "torch": "PyTorch",
    "cv2": "OpenCV",
    "mmengine": "MMEngine",
    "mmcv": "MMCV",
    "mmpose": "MMPose",
}


def missing_dependencies() -> list[str]:
    missing: list[str] = []
    for module_name, label in REQUIRED_MODULES.items():
        if find_spec(module_name) is None:
            missing.append(f"{label} ({module_name})")
    return missing


def generate(source: str) -> dict[str, Any]:
    missing = missing_dependencies()
    if missing:
        joined = ", ".join(missing)
        raise BackendUnavailableError(
            "RTMPose backend is not installed. Missing: "
            f"{joined}. Install these in an external worker environment, "
            "then rerun with --backend rtmpose."
        )

    raise BackendUnavailableError(
        "RTMPose dependencies appear importable, but real inference is not "
        f"implemented yet for source: {source}"
    )
