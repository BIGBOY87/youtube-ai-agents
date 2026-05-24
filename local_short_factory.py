
"""
BANG IT UP MUSIC - Local Short Factory v15

Runs on your Windows PC, not on Render.

What it does:
- takes your own local MP4 file
- cuts 15-25 second Shorts
- converts to 9:16 vertical
- saves ready Short MP4 files
- creates upload JSON payloads for Render

Install:
pip install moviepy==1.0.3

Example:
python local_short_factory.py --input "C:\Videos\my_track.mp4" --title "MIDNIGHT RUN" --start 30 --duration 20
"""

import argparse
import json
import os
import re
from pathlib import Path
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip, TextClip

def safe_name(text):
    text = re.sub(r"[^a-zA-Z0-9_\- ]+", "", text).strip().replace(" ", "_")
    return text[:60] or "short"

def make_vertical_short(input_path, title, start, duration, output_dir="shorts_output"):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(str(input_path))

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    clip = VideoFileClip(str(input_path))
    end = min(float(start) + float(duration), clip.duration)
    sub = clip.subclip(float(start), end)

    target_w, target_h = 1080, 1920

    # Resize to fill vertical canvas.
    scale = max(target_w / sub.w, target_h / sub.h)
    resized = sub.resize(scale)
    x_center = resized.w / 2
    y_center = resized.h / 2
    cropped = resized.crop(
        x_center=x_center,
        y_center=y_center,
        width=target_w,
        height=target_h
    )

    # Top text overlay.
    try:
        txt = TextClip(
            title[:44],
            fontsize=70,
            color="white",
            font="Arial-Bold",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            size=(980, None),
            align="center"
        ).set_position(("center", 120)).set_duration(cropped.duration)
        final = CompositeVideoClip([cropped, txt], size=(target_w, target_h))
    except Exception:
        final = cropped

    out_file = out_dir / f"{safe_name(title)}_{int(start)}s_{int(duration)}s_SHORT.mp4"
    final.write_videofile(
        str(out_file),
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="veryfast",
        threads=4
    )

    clip.close()
    sub.close()
    final.close()

    payload = {
        "short_mp4_local_file": str(out_file.resolve()),
        "title": f"{title} #Shorts",
        "description": f"{title} by BANG IT UP MUSIC. #Shorts #BANGITUPMUSIC #TechHouse #EDM",
        "tags": ["BANGITUPMUSIC", "Shorts", "TechHouse", "EDM", "MelodicTechno"],
        "privacy_status": "private",
        "own_content_confirmed": True,
        "note": "Upload this MP4 to Drive/Dropbox/Cloudinary, then send the direct MP4 URL to /api/shorts/upload-from-url."
    }

    payload_file = out_dir / f"{safe_name(title)}_{int(start)}s_payload.json"
    payload_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("DONE")
    print("Short MP4:", out_file.resolve())
    print("Payload JSON:", payload_file.resolve())
    return str(out_file.resolve())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to your own local MP4 file")
    parser.add_argument("--title", required=True, help="Short title")
    parser.add_argument("--start", type=float, default=30, help="Start time in seconds")
    parser.add_argument("--duration", type=float, default=20, help="Duration in seconds")
    parser.add_argument("--output-dir", default="shorts_output")
    args = parser.parse_args()

    make_vertical_short(args.input, args.title, args.start, args.duration, args.output_dir)

if __name__ == "__main__":
    main()
