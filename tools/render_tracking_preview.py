"""Render a cached pose-tracking JSON as an SVG preview.

Usage:
    python tools/render_tracking_preview.py --input <json> --output <svg>

Stdlib-only. No external dependencies.
"""

import argparse
import json
import sys


# COCO-17 skeleton edge pairs, matching the schema's keypoint order.
SKELETON_GROUPS = {
    "head": [
    (0, 1), (0, 2),       # nose -> L-eye, R-eye
    (1, 3), (2, 4),       # L-eye -> L-ear, R-eye -> R-ear
    ],
    "arms": [
        (5, 7), (7, 9),       # L-shoulder -> L-elbow -> L-wrist
        (6, 8), (8, 10),      # R-shoulder -> R-elbow -> R-wrist
        (5, 6),               # shoulder bar
    ],
    "torso": [
        (5, 11), (6, 12),     # shoulders -> hips
        (11, 12),             # hip bar
    ],
    "legs": [
        (11, 13), (13, 15),   # L-hip -> L-knee -> L-ankle
        (12, 14), (14, 16),   # R-hip -> R-knee -> R-ankle
    ],
}
CHAIN_COLORS = {
    "arms": "#4488ff",
    "legs": "#f08040",
    "torso": "#44bb44",
    "head": "#cc44cc",
}

# COCO keypoint names for labels
KP_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


def render(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["video_meta"]
    w, h = meta["width"], meta["height"]
    frames = data["frames"]

    # Use first frame for preview
    frame = frames[0]
    fw, fh = frame["width"], frame["height"]
    persons = frame["persons"]

    # SVG dimensions
    pad = 60
    svg_w = fw + pad * 2
    svg_h = fh + pad * 2

    lines = []
    elems = []

    def _line(x1, y1, x2, y2, color, sw=2.5, dash=""):
        style = f'stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round"'
        if dash:
            style += f' stroke-dasharray="{dash}"'
        return f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {style}/>'

    def _circle(cx, cy, r, fill):
        return f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="#fff" stroke-width="1.2"/>'

    def _rect(x, y, rw, rh, stroke):
        return f'  <rect x="{x:.0f}" y="{y:.0f}" width="{rw:.0f}" height="{rh:.0f}" fill="none" stroke="{stroke}" stroke-width="2" rx="4"/>'

    # SVG header
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">')
    lines.append(f'  <rect width="100%" height="100%" fill="#1a1a2e"/>')

    # Title
    lines.append('  <text x="30" y="30" font-family="sans-serif" font-size="16" fill="#eee" text-anchor="start">Frame {} | persons: {} | source: {}</text>'.format(
        frame["frame_index"], len(persons), meta.get("source", "n/a")
    ))

    # Track iters
    for ti, person in enumerate(persons):
        track_id = person.get("track_id", "?")
        track_color = ["#4488ff", "#f08040", "#44bb44", "#cc4466", "#66bbcc", "#ee6644"][ti % 6]
        kp_pts = []
        for kp in person["keypoints"]:
            px = pad + kp["x"] * fw
            py = pad + kp["y"] * fh
            kp_pts.append((px, py))

        # Bounding box
        b = person["bbox"]
        bx = pad + b["x"] * fw
        by = pad + b["y"] * fh
        bw = b["width"] * fw
        bh = b["height"] * fh
        elems.append(_rect(bx, by, bw, bh, track_color))

        # Skeleton lines by chain.
        for chain_name, chain in SKELETON_GROUPS.items():
            color = CHAIN_COLORS[chain_name]
            for a, b_idx in chain:
                if a < len(kp_pts) and b_idx < len(kp_pts):
                    elems.append(_line(kp_pts[a][0], kp_pts[a][1], kp_pts[b_idx][0], kp_pts[b_idx][1], color, 2.5))

        # Keypoint circles
        for pi, (px, py) in enumerate(kp_pts):
            score = person["keypoints"][pi]["score"]
            if score > 0.9:
                fill = "white"
            elif score > 0.6:
                fill = "#aaa"
            else:
                fill = "#666"
            elems.append(_circle(px, py, 4, fill))

        # Track ID label
        if len(kp_pts) >= 10:
            cx = sum(p[0] for p in kp_pts) / len(kp_pts)
            cy = min(p[1] for p in kp_pts) - 10
        elif len(kp_pts) >= 1:
            cx = kp_pts[0][0]
            cy = kp_pts[0][1] - 10
        else:
            cx = pad
            cy = pad + 20
        label = f"T{track_id}"
        elems.append(f'    <text x="{cx:.0f}" y="{cy:.0f}" font-family="sans-serif" font-size="13" fill="{track_color}" font-weight="bold" text-anchor="middle">{label}</text>')

    # Keypoint name labels on the last person
    if persons:
        last_person = persons[-1]
        for pi, kp in enumerate(last_person["keypoints"]):
            px = pad + kp["x"] * fw
            py = pad + kp["y"] * fh
            # offset label away from joint
            ox, oy = -12, -10
            if pi in (11, 12):  # hips, push down
                oy = 18
            if pi in (13, 14):  # knees, push down
                oy = 18
            name = KP_NAMES[pi]
            elems.append(f'    <text x="{px + ox:.0f}" y="{py + oy:.0f}" font-family="monospace" font-size="9" fill="#ccc" text-anchor="start">{name}</text>')

    # Footer
    lines.append('  <text x="30" y="{}" font-family="monospace" font-size="10" fill="#888" text-anchor="start">Normalized coords | COCO-17 | {} frames total</text>'.format(
        svg_h - 15, len(frames)
    ))

    lines.append('  <text x="{}" y="{}" font-family="monospace" font-size="10" fill="#888" text-anchor="end">Motion Tracking Preview</text>'.format(
        svg_w - 30, svg_h - 15
    ))

    # Insert drawn elements before closing tag
    for e in elems:
        lines.append(e)

    # Write output
    lines.append('</svg>')
    svg_content = "\n".join(lines) + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Wrote: {output_path}")
    print(f"  {len(frames)} frame(s), {sum(len(fr['persons']) for fr in frames)} person(s) total")


def main():
    parser = argparse.ArgumentParser(description="Render cached pose tracking JSON as SVG preview")
    parser.add_argument("--input", required=True, help="Path to tracking result JSON")
    parser.add_argument("--output", required=True, help="Output SVG path")
    args = parser.parse_args()

    try:
        render(args.input, args.output)
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
