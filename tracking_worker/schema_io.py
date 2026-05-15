"""Schema-aware JSON reading and writing for tracking results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_SCHEMA_REL = "schemas/tracking_result.schema.json"


def _find_repo_root() -> Path:
    here = Path(__file__).resolve().parent
    for parent in (here, *here.parents):
        if (parent / ".git").is_dir():
            return parent
    return here


def _load_schema() -> dict[str, Any]:
    root = _find_repo_root()
    schema_path = root / _SCHEMA_REL
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_tracking_json(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Lite validation against the schema rules (stdlib only).

    Returns (ok, errors).
    """
    schema = _load_schema()
    required_keys = schema.get("required", [])
    errors: list[str] = []

    if not isinstance(data, dict):
        return False, ["Top-level must be an object"]

    for rk in required_keys:
        if rk not in data:
            errors.append(f"Missing required key: {rk}")

    if errors:
        return False, errors

    # video_meta
    if "video_meta" in data:
        meta = data["video_meta"]
        if not isinstance(meta, dict):
            errors.append("video_meta must be an object")
        else:
            meta_required = schema.get("properties", {}).get("video_meta", {}).get("required", [])
            for mk in meta_required:
                if mk not in meta:
                    errors.append(f"video_meta missing required field: {mk}")
            for wfield in ("width", "height"):
                val = meta.get(wfield)
                if isinstance(val, (int, float)):
                    if val < 1:
                        errors.append(f"video_meta.{wfield} must be >= 1")

    # frames
    if "frames" in data:
        frames = data["frames"]
        if not isinstance(frames, list):
            errors.append("frames must be an array")
        elif len(frames) < 1:
            errors.append("frames array must have at least 1 item")
        else:
            frame_required = schema.get("properties", {}).get("frames", {}).get("items", {}).get("required", [])
            for fi, frame in enumerate(frames):
                if not isinstance(frame, dict):
                    errors.append(f"Frame {fi}: must be an object")
                    continue
                for fk in frame_required:
                    if fk not in frame:
                        errors.append(f"Frame {fi}: missing required: {fk}")

                persons = frame.get("persons", [])
                if not isinstance(persons, list) or len(persons) < 1:
                    errors.append(f"Frame {fi}: 'persons' must be non-empty")
                else:
                    person_schema = schema.get("properties", {}).get("frames", {}).get("items", {}).get("properties", {}).get("persons", {}).get("items", {})
                    person_required = person_schema.get("required", [])
                    kp_schema = person_schema.get("properties", {}).get("keypoints", {})
                    kp_required = kp_schema.get("items", {}).get("required", [])
                    bbox_schema = person_schema.get("properties", {}).get("bbox", {})
                    bbox_required = bbox_schema.get("required", [])

                    for pi, person in enumerate(persons):
                        if not isinstance(person, dict):
                            errors.append(f"Frame {fi}, Person {pi}: must be object")
                            continue
                        for pk in person_required:
                            if pk not in person:
                                errors.append(f"Frame {fi}, Person {pi}: missing: {pk}")

                        kps = person.get("keypoints")
                        if isinstance(kps, list):
                            if len(kps) != 17:
                                errors.append(f"Frame {fi}, Person {pi}: keypoints must be 17, got {len(kps)}")
                            else:
                                for ki, kp in enumerate(kps):
                                    if not isinstance(kp, dict):
                                        errors.append(f"Frame {fi}, Person {pi}, KP {ki}: must be object")
                                        continue
                                    for kkk in kp_required:
                                        if kkk not in kp:
                                            errors.append(f"Frame {fi}, Person {pi}, KP {ki}: missing: {kkk}")

                        bbox = person.get("bbox")
                        if isinstance(bbox, dict):
                            for bk in bbox_required:
                                if bk not in bbox:
                                    errors.append(f"Frame {fi}, Person {pi}: bbox missing: {bk}")

    return len(errors) == 0, errors


def write_tracking_result(data: dict[str, Any], output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
