import os
import subprocess

def process_media_info(file_path, width, script_directory):
    """Processes media files based on resolution and re-encodes them using HandBrakeCLI."""
    
    width = int(width)  # Ensure width is treated as an integer
    preset_mapping = {
        'HD': ("Presets/SuperShrinkHD.json", "SuperShrinkHD"),
        '4K': ("Presets/SuperShrink4K.json", "SuperShrink4K")
    }
    
    # Determine appropriate preset based on width
    if width <= 1920:
        preset_file, preset_name = preset_mapping['HD']
    elif 1921 <= width <= 3840:
        preset_file, preset_name = preset_mapping['4K']
    else:
        print(f"[SKIPPED] {file_path} - Unsupported resolution: {width}px")
        return

    # Define paths
    handbrake_path = os.path.join(script_directory, "App", "HandBrakeCLI.exe")
    reencoded_directory = os.path.join(script_directory, "ReEncodedFiles", os.path.splitext(os.path.basename(file_path))[0])
    os.makedirs(reencoded_directory, exist_ok=True)
    
    output_file_path = os.path.join(reencoded_directory, os.path.splitext(os.path.basename(file_path))[0] + "_converted.mkv")
    preset_file_full_path = os.path.join(script_directory, preset_file)

    # Run HandBrakeCLI without capturing output so you see it on the console
    arguments = [
        handbrake_path, '-i', file_path, '-o', output_file_path,
        '--preset-import-file', preset_file_full_path, '--preset', preset_name, '--verbose=1'
    ]

    print(f"[PROCESSING] Encoding {file_path} -> {output_file_path} using {preset_name}...")

    try:
        # Remove stdout/stderr capturing to display real-time output
        subprocess.run(arguments, check=True)
        print(f"[SUCCESS] Re-encoded: {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] HandBrakeCLI failed for {file_path}: {e}")

# Main script execution
script_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_directory, "TXT", "FilesToBeProcessed_v2.txt")

if os.path.exists(text_file_path):
    with open(text_file_path, 'r') as file:
        video_files = [line.strip().strip('"') for line in file if line.strip()]

    # Process each file
    for file_path in video_files:
        if os.path.exists(file_path):
            ffprobe_path = os.path.join(script_directory, "App", "ffprobe.exe")
            try:
                result = subprocess.run(
                    [ffprobe_path, '-v', 'error', '-select_streams', 'v:0',
                     '-show_entries', 'stream=codec_name,width',
                     '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
                    capture_output=True, text=True, check=True
                )
                
                output = result.stdout.strip().split('\n')
                if len(output) == 2:
                    width = output[1].strip()  # Extract width value
                    process_media_info(file_path, width, script_directory)
                else:
                    print(f"[WARNING] ffprobe could not retrieve valid info for: {file_path}")

            except subprocess.CalledProcessError:
                print(f"[ERROR] ffprobe failed for {file_path}. Skipping...")
        else:
            print(f"[MISSING] File not found: {file_path}")
else:
    print(f"[ERROR] Input file list not found: {text_file_path}")
