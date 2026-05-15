# COCO 17 standard body joints in keypoint index order.
KEYPOINT_NAMES = (
    "nose",
    "left_eye", "right_eye",
    "left_ear", "right_ear",
    "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow",
    "left_wrist", "right_wrist",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
)


def import_poses(filepath: str) -> dict:
    """Load and return parsed pose data from a cached JSON file.

    Raises
    ------
    FileNotFoundError
        If the path does not exist.
    ValueError
        If the JSON structure does not match the expected contract.
    """
    import os
    import json

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"pose JSON not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    # -- contract validation (lightweight, no schema lib) --
    if "video_meta" not in data or "frames" not in data:
        raise ValueError("JSON must contain 'video_meta' and 'frames' keys")

    meta = data["video_meta"]
    for key in ("width", "height"):
        if key not in meta or not isinstance(meta[key], (int, float)):
            raise ValueError(f"video_meta.{key} must be numeric")

    frames = data["frames"]
    if not isinstance(frames, list) or len(frames) < 1:
        raise ValueError("frames must be a non-empty array")

    for fi, frame in enumerate(frames):
        for req in ("frame_index", "width", "height", "persons"):
            if req not in frame:
                raise ValueError(f"frames[{fi}] missing key '{req}'")
        if not isinstance(frame["persons"], list) or len(frame["persons"]) < 1:
            raise ValueError(f"frames[{fi}].persons must have >= 1 person")
        for pi, person in enumerate(frame["persons"]):
            for req in ("track_id", "keypoints", "score", "bbox"):
                if req not in person:
                    raise ValueError(f"frames[{fi}].persons[{pi}] missing '{req}'")
            kps = person["keypoints"]
            if len(kps) != 17:
                raise ValueError(f"keypoints length is {len(kps)}, expected 17")
            for ki, kp in enumerate(kps):
                for k in ("x", "y", "score"):
                    if k not in kp:
                        raise ValueError(f"keypoint[{ki}] missing '{k}'")

    return data
