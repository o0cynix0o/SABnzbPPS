import os
import subprocess
import json
import requests
import time
import logging
import sys
from datetime import datetime

# ══════════════════════════════════════════════
# 🔐 SECTION 1: API Configuration and Constants
# ══════════════════════════════════════════════

# Radarr API configuration
RADARR_API_KEY = "4309795e4f7a4045bd1cf652a17e66bf"
RADARR_URL = "http://localhost:55004/api/v3/command"
RADARR_DELAY_TIME = 5  # Delay (in seconds) after notifying Radarr

# ══════════════════════════════════════════════
# 📁 SECTION 2: Path Setup
# ══════════════════════════════════════════════

# Base directory where the script is located
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Input file containing list of movies to be processed
TEXT_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, "TXT", "MoviesToBeProcessed.txt")

# Paths to required binaries
FFPROBE_PATH = os.path.join(SCRIPT_DIRECTORY, "App", "ffprobe.exe")
HANDBRAKE_PATH = os.path.join(SCRIPT_DIRECTORY, "App", "HandBrakeCLI.exe")

# Output directory for re-encoded files
RE_ENCODED_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "ReEncodedFiles")

# Create timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, "Log", f"encode_log_{timestamp}.txt")

# ══════════════════════════════════════════════
# 📝 SECTION 3: Logging Setup
# ══════════════════════════════════════════════

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Clear any existing handlers
logger.handlers.clear()

# Create formatters
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

# Create file handler
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ══════════════════════════════════════════════
# 🎛️ SECTION 4: HandBrake Preset Mapping
# ══════════════════════════════════════════════

# Map resolutions to preset files
PRESET_MAPPING = {
    'HD': {"preset_file": "Presets/SuperShrinkHD.json", "preset_name": "SuperShrinkHD"},
    '4K': {"preset_file": "Presets/SuperShrink4K.json", "preset_name": "SuperShrink4K"}
}

# ══════════════════════════════════════════════
# 🔍 SECTION 5: Get Video Info
# ══════════════════════════════════════════════

def get_video_info(file_path):
    """
    Uses ffprobe to retrieve codec and width of the video stream.
    Returns a (codec, width) tuple or (None, None) on failure.
    """
    ffprobe_args = [
        FFPROBE_PATH, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    try:
        result = subprocess.run(ffprobe_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip().splitlines()
        if len(output) >= 2:
            codec = output[0].strip()
            width = int(output[1].strip())
            return codec, width
        else:
            logger.warning(f"ffprobe returned insufficient data for: {file_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"ffprobe failed for {file_path}: {e}")
    except ValueError as e:
        logger.error(f"Invalid width returned by ffprobe for {file_path}: {e}")
    return None, None

# ══════════════════════════════════════════════
# 🎥 SECTION 6: Media Processing Function
# ══════════════════════════════════════════════

def process_media_info(file_path, codec, width):
    """
    Processes a media file using HandBrakeCLI based on its resolution.
    - Selects preset based on width
    - Encodes video using HandBrake
    - Streams output to console and logs
    - Notifies Radarr after encoding
    """
    logger.info(f"Processing file: {file_path}")
    logger.info(f"Video codec: {codec}, Width: {width} pixels")
    logger.info("-" * 50)

    # Determine which preset to use
    preset = PRESET_MAPPING['HD'] if int(width) <= 1920 else PRESET_MAPPING.get('4K')
    if not preset:
        logger.warning("Video width does not match preset conditions. Skipping file.")
        return

    # Ensure output directory exists
    os.makedirs(RE_ENCODED_DIRECTORY, exist_ok=True)

    # Construct output path
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = os.path.join(RE_ENCODED_DIRECTORY, f"{file_name}_converted.mkv")
    preset_file_full_path = os.path.join(SCRIPT_DIRECTORY, preset["preset_file"])

    # Build HandBrakeCLI command
    arguments = [
        HANDBRAKE_PATH, "-i", file_path, "-o", output_file_path,
        "--preset-import-file", preset_file_full_path,
        "--preset", preset["preset_name"], "--verbose=1"
    ]

    logger.info(f"Starting HandBrakeCLI processing with preset '{preset['preset_name']}'")

    try:
        # Stream HandBrake output in real-time to console and log
        process = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Process output line by line
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Strip newlines and log the HandBrake output
                line = output.strip()
                if line:
                    logger.info(f"HandBrake: {line}")
                    # Also flush to ensure real-time output
                    sys.stdout.flush()
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            logger.info(f"Processing completed: {output_file_path}")
        else:
            logger.error(f"HandBrakeCLI failed with return code {return_code}")
            return
            
    except Exception as e:
        logger.error(f"HandBrakeCLI failed: {e}")
        return

    # Notify Radarr when encoding is complete
    notify_radarr(output_file_path)

# ══════════════════════════════════════════════
# 📡 SECTION 7: Notify Radarr Function
# ══════════════════════════════════════════════

def notify_radarr(output_file_path):
    """
    Notifies Radarr to scan the folder containing the processed file.
    - Sends POST request to Radarr API
    - Waits for Radarr to possibly move/delete the file
    - Logs result
    """
    json_payload = {"name": "DownloadedMoviesScan", "path": output_file_path}
    try:
        response = requests.post(RADARR_URL, headers={"X-Api-Key": RADARR_API_KEY}, json=json_payload)
        response.raise_for_status()
        logger.info(f"Radarr Response: {response.json()}")
        time.sleep(RADARR_DELAY_TIME)

        # If file was imported (i.e., removed), note that
        if not os.path.exists(output_file_path):
            logger.info(f"File {output_file_path} successfully imported by Radarr.")
        else:
            logger.warning(f"File {output_file_path} not imported by Radarr.")
    except requests.RequestException as e:
        logger.error(f"Failed to send request to Radarr: {e}")

# ══════════════════════════════════════════════
# 🚀 SECTION 8: Main Function
# ══════════════════════════════════════════════

def main():
    """
    Main function that:
    - Loads video paths from the TXT file
    - Uses ffprobe to extract codec and width
    - Passes media info to the processor function
    """
    logger.info("========== Script Started ==========")

    # Check if input list exists
    if not os.path.exists(TEXT_FILE_PATH):
        logger.error(f"Text file not found: {TEXT_FILE_PATH}")
        return

    # Read paths from file
    with open(TEXT_FILE_PATH, 'r') as file:
        video_files = [line.strip().strip('"') for line in file if line.strip()]

    # Process each video file
    for file_path in video_files:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue

        codec, width = get_video_info(file_path)
        if codec is None or width is None:
            logger.warning(f"Skipping file due to missing metadata: {file_path}")
            continue

        if width <= 3840:
            process_media_info(file_path, codec, width)
        else:
            logger.warning(f"Video resolution unsupported: {width}px")

    logger.info("========== Script Finished ==========")

# ══════════════════════════════════════════════
# 🧷 Entry Point
# ══════════════════════════════════════════════

if __name__ == "__main__":
    main()
