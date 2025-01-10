import os
import subprocess
import json
import requests
import time

def process_media_info(file_path, codec, width, script_directory, category):
    """
    Processes the video file using HandBrakeCLI and sends a scan request to Sonarr or Radarr based on the category.
    """
    # Define presets based on video width
    if int(width) <= 1920:
        preset_file = "Presets/SuperShrinkHD.json"
        preset_name = "SuperShrinkHD"
    elif 1921 <= int(width) <= 3840:
        preset_file = "Presets/SuperShrink4K.json"
        preset_name = "SuperShrink4K"
    else:
        print("Video width does not match preset conditions. Skipping file.")
        return

    # Define paths for HandBrakeCLI processing
    handbrake_path = os.path.join(script_directory, "App", "HandBrakeCLI.exe")
    reencoded_directory = os.path.join(script_directory, "ReEncodedFiles", os.path.splitext(os.path.basename(file_path))[0])
    os.makedirs(reencoded_directory, exist_ok=True)
    
    # Set output file path for converted video
    output_file_path = os.path.join(reencoded_directory, os.path.splitext(os.path.basename(file_path))[0] + "_converted.mkv")
    preset_file_full_path = os.path.join(script_directory, preset_file)

    # Arguments for HandBrakeCLI
    arguments = [handbrake_path, '-i', file_path, '-o', output_file_path, '--preset-import-file', preset_file_full_path, '--preset', preset_name, '--verbose=1']
    subprocess.run(arguments, check=True)

    # API call based on category (Sonarr or Radarr)
    if category == "TVShows":
        # Placeholder API key for Sonarr (replace with actual API key)
        sonarr_api_key = "your_sonarr_api_key_here"
        sonarr_url = "http://localhost:port#/api/v3/command"
        json_payload = {"name": "downloadedepisodesscan", "path": output_file_path}
        api_url = sonarr_url
        api_key = sonarr_api_key
    elif category == "Movies":
        # Placeholder API key for Radarr (replace with actual API key)
        radarr_api_key = "your_radarr_api_key_here"
        radarr_url = "http://localhost:port#/api/v3/command"
        json_payload = {"name": "downloadedmoviesscan", "path": output_file_path}
        api_url = radarr_url
        api_key = radarr_api_key
    else:
        print(f"Unknown category: {category}. Skipping API call.")
        return

    # Send request to Sonarr or Radarr API
    try:
        response = requests.post(api_url, headers={"X-Api-Key": api_key}, json=json_payload)
        response.raise_for_status()

        time.sleep(5)
        if not os.path.exists(output_file_path):
            if not os.listdir(reencoded_directory):
                os.rmdir(reencoded_directory)
    except requests.RequestException as e:
        print(f"Failed to send request: {e}")

# Main script execution
script_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_directory, "TXT", "FilesToBeProcessed.txt")

if os.path.exists(text_file_path):
    with open(text_file_path, 'r') as file:
        lines = [line.strip().strip('"') for line in file.readlines()]

        if len(lines) % 2 != 0:
            print("The number of lines in the text file should be even (file path followed by category).")
        else:
            for i in range(0, len(lines), 2):
                file_path = lines[i]
                category = lines[i + 1]

                if os.path.exists(file_path):
                    ffprobe_path = os.path.join(script_directory, "App", "ffprobe.exe")
                    result = subprocess.run([ffprobe_path, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
                    output = result.stdout.strip().split('\n')
                    
                    if len(output) == 2:
                        codec, width = map(str.strip, output)
                        process_media_info(file_path, codec, width, script_directory, category)
                    else:
                        print(f"ffprobe could not retrieve information for: {file_path}")
                else:
                    print(f"File not found: {file_path}")
else:
    print(f"Text file not found at path: {text_file_path}")
