# Snapchat Export Overlay Merger

Merges Snapchat overlay PNG files onto their corresponding base images and videos from a Snapchat data export.

## What it does

Snapchat data exports include media files split into two parts:

- `<name>-main.jpg` / `<name>-main.mp4` — the base photo or video
- `<name>-overlay.png` — the overlay (stickers, text, filters, etc.)

This script composites each overlay onto its matching base file and saves the result to an output directory. Files that have no matching overlay are copied as-is.

## Requirements

- Python 3.8 or newer
- ffmpeg (required for video merging) — install via your package manager:
  - **Debian/Ubuntu:** `sudo apt install ffmpeg`
  - **macOS:** `brew install ffmpeg`
  - **Windows:** download from https://ffmpeg.org/download.html

## Setup

1. Clone or download this repository.

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Place all your Snapchat export files (`*-main.jpg`, `*-main.mp4`, `*-overlay.png`) into a single directory, then run:

```bash
python merge_overlays.py /path/to/your/snapchat/exports
```

The merged files will be saved to `merged_snapchat_exports/` in the current directory by default.

To specify a custom output directory:

```bash
python merge_overlays.py /path/to/your/snapchat/exports -o /path/to/output
```

## Output

- Files with a matching overlay: merged and saved to the output directory.
- Files without a matching overlay: copied as-is to the output directory.
