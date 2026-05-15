"""Validate a tracking result JSON file against the schema rules.

Usage:
    python tools/validate_tracking_json.py <path>

Pass/fail: prints PASS or FAIL with per-field details.
"""

import argparse
import json
import sys


REQUIRED_VIDEO_META = {"width", "height"}
REQUIRED_FRAME_FIELDS = {"frame_index", "width", "height", "persons"}
REQUIRED_PERSON_FIELDS = {"track_id", "keypoints", "score", "bbox"}
REQUIRED_KEYPOINT_FIELDS = {"x", "y", "score"}
REQUIRED_BBOX_FIELDS = {"x", "y", "width", "height"}
EXACT_KEYPOINTS = 17


def check_range(val, lo, hi, label):
    """Check a value is in [lo, hi] or [lo, inf) if hi is None. Return (ok, msg)."""
    if val < lo:
        return False, f"{label} below minimum {lo}: {val}"
    if hi is not None and val > hi:
        return False, f"{label} above maximum {hi}: {val}"
    return True, None


def validate(keypoint):
    """Validata a single keypoint dict."""
    errs = []
    for field in REQUIRED_KEYPOINT_FIELDS:
        if field not in keypoint:
            errs.append(f"keypoint missing '{field}'")
    if not errs:
        ok, msg = check_range(keypoint["x"], 0, 1, "x")
        if not ok:
            errs.append(msg)
        ok, msg = check_range(keypoint["y"], 0, 1, "y")
        if not ok:
            errs.append(msg)
        ok, msg = check_range(keypoint["score"], 0, 1, "keypoint.score")
        if not ok:
            errs.append(msg)
    return errs


def validate_bbox(bbox):
    """Validate a bbox dict."""
    errs = []
    for field in REQUIRED_BBOX_FIELDS:
        if field not in bbox:
            errs.append(f"bbox missing '{field}'")
    if not errs:
        ok, msg = check_range(bbox["x"], 0, 1, "bbox.x")
        if not ok:
            errs.append(msg)
        ok, msg = check_range(bbox["y"], 0, 1, "bbox.y")
        if not ok:
            errs.append(msg)
        ok, msg = check_range(bbox["width"], 0, 1, "bbox.width")
        if not ok:
            errs.append(msg)
        ok, msg = check_range(bbox["height"], 0, 1, "bbox.height")
        if not ok:
            errs.append(msg)
    return errs


def validate_file(path):
    """Validate a tracking result JSON. Return (success, errors)."""
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False, [f"File not found: {path}"]
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]

    if not isinstance(data, dict):
        return False, ["Top-level should be an object"]

    # video_meta
    if "video_meta" not in data:
        errors.append("Missing 'video_meta'")
    else:
        meta = data["video_meta"]
        if not isinstance(meta, dict):
            errors.append("video_meta should be an object")
        else:
            for field in REQUIRED_VIDEO_META:
                if field not in meta:
                    errors.append(f"video_meta missing '{field}'")
                else:
                    ok, msg = check_range(meta[field], 1, None, f"video_meta.{field}")
                    if ok is False:
                        errors.append(msg)

    # frames
    if "frames" not in data:
        errors.append("Missing 'frames'")
    else:
        frames = data["frames"]
        if not isinstance(frames, list):
            errors.append("frames should be an array")
        else:
            if len(frames) < 1:
                errors.append("frames array must have at least 1 item")
            for i, frame in enumerate(frames):
                if not isinstance(frame, dict):
                    errors.append(f"Frame {i}: should be an object")
                    continue
                for field in REQUIRED_FRAME_FIELDS:
                    if field not in frame:
                        errors.append(f"Frame {i} missing '{field}'")
                for field in ("width", "height"):
                    if field in frame:
                        ok, msg = check_range(frame[field], 1, None, f"frame[{i}].{field}")
                        if ok is False:
                            errors.append(msg)
                if "frame_index" in frame and not isinstance(frame["frame_index"], int):
                    errors.append(f"Frame {i}.frame_index should be integer")

                # persons
                if "persons" not in frame or not isinstance(frame["persons"], list):
                    errors.append(f"Frame {i}: missing or invalid 'persons' array")
                    continue

                for j, person in enumerate(frame["persons"]):
                    if not isinstance(person, dict):
                        errors.append(f"Frame {i}, Person {j}: should be an object")
                        continue

                    for field in REQUIRED_PERSON_FIELDS:
                        if field not in person:
                            errors.append(f"Frame {i}, Person {j} missing '{field}'")

                    # track_id
                    if "track_id" in person:
                        tid = person["track_id"]
                        if tid is not None and not isinstance(tid, int):
                            errors.append(
                                f"Frame {i}, Person {j}.track_id: "
                                f"expected null or int, got {type(tid).__name__}"
                            )

                    # score
                    if "score" in person:
                        ok, msg = check_range(
                            person["score"], 0, 1,
                            f"frame[{i}].persons[{j}].score"
                        )
                        if ok is False:
                            errors.append(msg)

                    # keypoints
                    if "keypoints" in person:
                        kps = person["keypoints"]
                        if not isinstance(kps, list):
                            errors.append(
                                f"Frame {i}, Person {j}.keypoints: expected array"
                            )
                        else:
                            if len(kps) != EXACT_KEYPOINTS:
                                errors.append(
                                    f"Frame {i}, Person {j}: expected {EXACT_KEYPOINTS} "
                                    f"keypoints, got {len(kps)}"
                                )
                            else:
                                for ki, kp in enumerate(kps):
                                    kp_errs = validate(kp)
                                    for e in kp_errs:
                                        errors.append(f"Frame {i}, Person {j}, "
                                                     f"keypoint {ki}: {e}")

                    # bbox
                    if "bbox" in person:
                        bbox_errs = validate_bbox(person["bbox"])
                        for e in bbox_errs:
                            errors.append(f"Frame {i}, Person {j}: {e}")

    success = len(errors) == 0
    return success, errors


def main():
    parser = argparse.ArgumentParser(description="Validate tracking result JSON")
    parser.add_argument("path", help="Path to the tracking result JSON file")
    args = parser.parse_args()

    success, errors = validate_file(args.path)

    if success:
        # Print summary stats
        with open(args.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        frames = data.get("frames", [])
        total_persons = 0
        for frame in frames:
            total_persons += len(frame.get("persons", []))
        print(f"PASS: {args.path}")
        print(f"  Frames: {len(frames)}")
        print(f"  Total persons: {total_persons}")
        if "video_meta" in data:
            meta = data["video_meta"]
            print(f"  Source: {meta.get('source', 'n/a')} "
                  f"({meta.get('width', '?')}x{meta.get('height', '?')} @ "
                  f"{meta.get('fps', '?')} fps)")
        return 0
    else:
        print("FAIL:")
        for err in errors:
            print(f"  ERROR: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
