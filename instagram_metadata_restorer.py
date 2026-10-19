import os
import re
from datetime import datetime

def process_html_file(html_filepath, base_dir):
    with open(html_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The HTML groups each post inside a specific block container
    blocks = content.split('<div class="pam ')

    updated_count = 0
    error_count = 0

    # Skip the first chunk as it contains the header, not posts
    for block in blocks[1:]:
        # Extract all media paths within the block
        # Look for both video and image links
        media_paths = re.findall(r'(?:src|href)="(media/[^"]+)"', block)
        
        # Deduplicate paths (href and src often point to the same file in a single post)
        media_paths = list(set(media_paths))
        
        # Extract the date string located at the bottom of the block
        date_match = re.search(r'<div class="_3-94 _a6-o">([^<]+)</div>', block)

        if media_paths and date_match:
            date_str = date_match.group(1).strip()

            try:
                # Convert the text string (e.g., "Sep 22, 2026 9:04 am") into a Unix timestamp
                dt = datetime.strptime(date_str, "%b %d, %Y %I:%M %p")
                timestamp = dt.timestamp()

                for media_rel_path in media_paths:
                    # Dynamically resolve the path to the media file
                    # We check relative to the HTML folder and its parent directories 
                    # to ensure we find the media regardless of the exact folder hierarchy
                    possible_paths = [
                        os.path.join(base_dir, media_rel_path),
                        os.path.join(base_dir, "..", media_rel_path),
                        os.path.join(base_dir, "..", "..", media_rel_path)
                    ]

                    file_found = False
                    for p in possible_paths:
                        p = os.path.normpath(p)
                        if os.path.exists(p):
                            # Apply the timestamp to the file's 'Date Modified' and 'Date Accessed'
                            os.utime(p, (timestamp, timestamp))
                            print(f"[OK] Updated: {os.path.basename(p)} -> {date_str}")
                            updated_count += 1
                            file_found = True
                            break

                    if not file_found:
                        print(f"[WARNING] Media file not found on disk: {media_rel_path}")
                        error_count += 1

            except ValueError:
                print(f"[ERROR] Could not parse the date format: '{date_str}'")
                error_count += 1
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred with {media_rel_path}: {e}")
                error_count += 1

    return updated_count, error_count

def main():
    print("=== Instagram Metadata Restorer ===")
    print("This script reads your Instagram HTML files and updates the 'Date Modified'")
    print("timestamp of the corresponding media files so photo apps sort them correctly.\n")

    folder_path = input("Enter the full path to the folder containing your HTML files (e.g., your_instagram_activity/media): ").strip()
    
    # Strip accidental quotes if the folder was dragged and dropped into the terminal
    folder_path = folder_path.strip('"').strip("'")

    if not os.path.isdir(folder_path):
        print(f"\n[!] Error: The directory '{folder_path}' does not exist.")
        input("\nPress Enter to exit...")
        return

    total_updated = 0
    total_errors = 0

    print("\nScanning for HTML files...\n")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.html'):
            html_filepath = os.path.join(folder_path, filename)
            print(f"--- Processing {filename} ---")
            updated, errors = process_html_file(html_filepath, folder_path)
            total_updated += updated
            total_errors += errors

    print("\n=== Process Completed ===")
    print(f"Successfully reassigned metadata to: {total_updated} files.")
    print(f"Errors or Missing Files: {total_errors}")

    # Keeps the window open at the end so you can review the logs
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()