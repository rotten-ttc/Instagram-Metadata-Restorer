Made with AI for personal use.

# Instagram Metadata Restorer

A lightweight, dependency-free Python script that restores the original chronological "Date Modified" metadata to media files downloaded via Instagram's data export tool. 

## The Problem
When downloading Instagram data exports, media files often lack embedded EXIF data and receive a "Date Modified" timestamp matching the exact moment you downloaded them. This causes photo management applications (like Apple Photos, Google Photos, or Windows Explorer) to sort your entire Instagram history as a single massive dump on the day of the download.

## The Solution
This script parses the `.html` files provided in your data export to locate the original date each post was published. It then links that date to the corresponding local video or image file and updates its OS-level timestamp, restoring correct chronological sorting.

## Prerequisites
- **Python 3.x** installed on your system.
- No external packages or libraries are required (runs entirely on standard Python built-ins like `os`, `re`, and `datetime`).

## Usage

1. **Extract** your downloaded Instagram data `.zip` file.
2. **Run** the script via your terminal or command prompt:
   ```bash
   python instagram_metadata_restorer.py
   ```
3. **Input the path:** When prompted, paste the absolute path to the folder containing your Instagram HTML files (for example, the `your_instagram_activity/content` or `posts` folder depending on your export structure).
4. The script will scan the HTML, locate the associated media files, and print a real-time log of the updated timestamps.

## How it Works
- **Parses HTML:** Slices the raw HTML code by post container blocks.
- **Extracts Data:** Uses Regular Expressions (Regex) to find media relative paths (`href` or `src` pointing to `media/`) and captures the human-readable date string at the bottom of the post block.
- **Updates OS Metadata:** Converts the text date into a Unix timestamp and applies it to the actual file on your disk using `os.utime()`. Supports single posts and multi-image carousels.
