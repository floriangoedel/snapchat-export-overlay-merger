import argparse
import shutil
import subprocess
from pathlib import Path

from PIL import Image
from tqdm import tqdm


def merge_image(main_path: Path, overlay_path: Path, output_path: Path):
    with Image.open(main_path).convert("RGBA") as base:
        with Image.open(overlay_path).convert("RGBA") as overlay:
            if overlay.size != base.size:
                overlay = overlay.resize(base.size, Image.LANCZOS)
            merged = Image.alpha_composite(base, overlay)
        merged.convert("RGB").save(output_path, "JPEG", quality=95)


def merge_video(main_path: Path, overlay_path: Path, output_path: Path):
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(main_path),
            "-i", str(overlay_path),
            "-filter_complex", "[1:v][0:v]scale2ref[ov][base];[base][ov]overlay=0:0",
            "-c:a", "copy",
            str(output_path),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Merge Snapchat overlay PNGs onto base JPEGs and MP4s"
    )
    parser.add_argument(
        "input_dir",
        help="Directory containing *-main.jpg/*-main.mp4 and *-overlay.png files",
    )
    parser.add_argument(
        "-o", "--output",
        default="merged_snapchat_exports",
        help="Output directory (default: merged_snapchat_exports)",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    main_files = sorted(
        list(input_dir.glob("*-main.jpg")) + list(input_dir.glob("*-main.mp4"))
    )
    if not main_files:
        print("No *-main.jpg or *-main.mp4 files found.")
        return

    merged = skipped = failed = 0
    for main_path in tqdm(main_files, desc="Merging", unit="file"):
        ext = main_path.suffix  # .jpg or .mp4
        stem = main_path.name[: -len(f"-main{ext}")]
        overlay_path = main_path.with_name(f"{stem}-overlay.png")
        out_path = output_dir / f"{stem}{ext}"

        if not overlay_path.exists():
            shutil.copy2(main_path, out_path)
            skipped += 1
            continue

        try:
            if ext == ".mp4":
                merge_video(main_path, overlay_path, out_path)
            else:
                merge_image(main_path, overlay_path, out_path)
            merged += 1
        except Exception as e:
            tqdm.write(f"Failed {main_path.name}: {e}")
            failed += 1

    print(f"\nMerged: {merged} | No overlay (copied): {skipped} | Failed: {failed}")


if __name__ == "__main__":
    main()
