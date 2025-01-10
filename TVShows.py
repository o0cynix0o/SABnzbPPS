import os
import subprocess
import json
import requests
import time

# Editable Variables

# Directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the text file containing the list of video files to be processed
text_file_path = os.path.join(script_directory, "TXT/ShowsToBeProcessed.txt")

# Path to the ffprobe executable used to gather video information
ffprobe_path = os.path.join(script_directory, "App/ffprobe.exe")

# Path to the HandBrakeCLI executable used for re-encoding video files
handbrake_path = os.path.join(script_directory, "App/HandBrakeCLI.exe")

# Retrieve Sonarr API key and URL from environment variables for security
sonarr_api_key = os.getenv("SONARR_API_KEY", "default_api_key")
sonarr_url = os.getenv("SONARR_URL", "http://localhost:55003/api/v3/command")

# Directory where re-encoded files will be stored
re_encoded_directory = os.path.join(script_directory, "ReEncodedFiles")

# Preset files for different video resolutions
preset_mapping = {
    'HD': {"preset_file": "Presets/SuperShrinkHD.json", "preset_name": "SuperShrinkHD"},
    '4K': {"preset_file": "Presets/SuperShrink4K.json", "preset_name": "SuperShrink4K"}
}

# Delay time (in seconds) after sending the request to Sonarr
sonarr_delay_time = 5

# Script Functions

def process_media_info(file_path, codec, width, script_directory):
    """
    Processes a media file using HandBrakeCLI based on its resolution.
    """
    print(f"Processing file: {file_path}")
    print(f"The video codec is {codec} and the width is {width} pixels.")
    print("----------------------------------------------")

    if int(width) <= 1920:
        preset = preset_mapping['HD']
    elif 1921 <= int(width) <= 3840:
        preset = preset_mapping['4K']
    else:
        print("Video width does not match preset conditions. Skipping file.")
        return

    os.makedirs(re_encoded_directory, exist_ok=True)

    file_directory_name = os.path.splitext(os.path.basename(file_path))[0]
    file_specific_directory = os.path.join(re_encoded_directory, file_directory_name)
    os.makedirs(file_specific_directory, exist_ok=True)

    output_file_path = os.path.join(file_specific_directory, f"{file_directory_name}_converted.mkv")
    preset_file_full_path = os.path.join(script_directory, preset["preset_file"])

    arguments = [
        handbrake_path, "-i", file_path, "-o", output_file_path,
        "--preset-import-file", preset_file_full_path,
        "--preset", preset["preset_name"], "--verbose=1"
    ]

    print(f"Starting HandBrakeCLI processing for file: {file_path} with {preset['preset_name']} preset.")
    subprocess.run(arguments, check=True)
    print(f"Processing completed for file: {output_file_path}")

    json_payload = {"name": "downloadedepisodesscan", "path": output_file_path}

    try:
        response = requests.post(sonarr_url, headers={"X-Api-Key": sonarr_api_key}, json=json_payload)
        response.raise_for_status()
        print(f"Response: {response.json()}")

        time.sleep(sonarr_delay_time)

        if not os.path.exists(output_file_path):
            print(f"File {output_file_path} successfully imported by Sonarr.")
            if not any(os.scandir(file_specific_directory)):
                os.rmdir(file_specific_directory)
                print(f"Deleted directory: {file_specific_directory}")
            else:
                print(f"Directory {file_specific_directory} is not empty, not deleting.")
        else:
            print(f"File {output_file_path} was not imported by Sonarr, directory will not be deleted.")
    except requests.RequestException as e:
        print(f"Failed to send request: {e}")

def main():
    """
    Main function to process video files listed in a text file.
    """
    if os.path.exists(text_file_path):
        with open(text_file_path, 'r') as file:
            video_files = file.readlines()
        
        for file_path in video_files:
            file_path = file_path.strip().strip('"')
            if os.path.exists(file_path):
                ffprobe_args = [
                    ffprobe_path, '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=codec_name,width', '-of', 'default=noprint_wrappers=1:nokey=1', file_path
                ]
                result = subprocess.run(ffprobe_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = result.stdout.strip().split('\n')

                if output and len(output) >= 2:
                    codec, width = output
                    if int(width) <= 1920 or 1921 <= int(width) <= 3840:
                        process_media_info(file_path, codec, width, script_directory)
                    else:
                        print("Video width does not match preset conditions. Skipping file.")
                else:
                    print(f"ffprobe could not retrieve information for: {file_path}")
            else:
                print(f"File not found: {file_path}")
    else:
        print(f"Text file not found at path: {text_file_path}")

if __name__ == "__main__":
    main()
