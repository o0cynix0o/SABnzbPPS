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

# Sonarr API Configuration
SONARR_API_KEY = "3689d41353b344018cbaa13c9f95c5dc"
SONARR_URL = "http://localhost:55003/api/v3/command"

# Radarr API Configuration
RADARR_API_KEY = "4309795e4f7a4045bd1cf652a17e66bf"
RADARR_URL = "http://localhost:55004/api/v3/command"

# Processing Configuration
API_DELAY_TIME = 5  # Delay after notifying API

# ══════════════════════════════════════════════
# 📁 SECTION 2: Path Setup
# ══════════════════════════════════════════════

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, "TXT", "FilesToBeProcessed.txt")
FFPROBE_PATH = os.path.join(SCRIPT_DIRECTORY, "App", "ffprobe.exe")
HANDBRAKE_PATH = os.path.join(SCRIPT_DIRECTORY, "App", "HandBrakeCLI.exe")
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

PRESET_MAPPING = {
    "HD": {"preset_file": "Presets/SuperShrinkHD.json", "preset_name": "SuperShrinkHD"},
    "4K": {"preset_file": "Presets/SuperShrink4K.json", "preset_name": "SuperShrink4K"}
}

# ══════════════════════════════════════════════
# 🎯 SECTION 5: API Configuration Mapping
# ══════════════════════════════════════════════

API_MAPPING = {
    "Shows": {
        "url": SONARR_URL,
        "api_key": SONARR_API_KEY,
        "command": "downloadedepisodesscan"
    },
    "Movies": {
        "url": RADARR_URL,
        "api_key": RADARR_API_KEY,
        "command": "downloadedmoviesscan"
    }
}

# ══════════════════════════════════════════════
# 🔍 SECTION 6: Get Video Info
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
# 🎥 SECTION 7: Process Media File
# ══════════════════════════════════════════════

def process_media_info(file_path, codec, width, category):
    """
    Re-encodes a video file using HandBrakeCLI and notifies appropriate API upon success.
    """
    logger.info(f"Processing file: {file_path}")
    logger.info(f"Video codec: {codec}, Width: {width}px, Category: {category}")
    logger.info("-" * 50)

    # Select preset based on resolution
    if width <= 1920:
        preset = PRESET_MAPPING['HD']
    elif 1921 <= width <= 3840:
        preset = PRESET_MAPPING['4K']
    else:
        logger.warning(f"Video width {width}px does not match preset conditions. Skipping file.")
        return

    # Create output directory for this file
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    reencoded_directory = os.path.join(RE_ENCODED_DIRECTORY, file_name)
    os.makedirs(reencoded_directory, exist_ok=True)
    
    output_file_path = os.path.join(reencoded_directory, f"{file_name}_converted.mkv")
    preset_file_full_path = os.path.join(SCRIPT_DIRECTORY, preset["preset_file"])

    arguments = [
        HANDBRAKE_PATH, "-i", file_path, "-o", output_file_path,
        "--preset-import-file", preset_file_full_path,
        "--preset", preset["preset_name"], "--verbose=1"
    ]

    logger.info(f"Running HandBrakeCLI with preset: {preset['preset_name']}")

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
            logger.info(f"Successfully re-encoded {file_path} to {output_file_path}")
        else:
            logger.error(f"HandBrakeCLI failed with return code {return_code}")
            return
            
    except Exception as e:
        logger.error(f"HandBrakeCLI failed for {file_path}: {e}")
        return

    notify_api(output_file_path, category, reencoded_directory)

# ══════════════════════════════════════════════
# 📡 SECTION 8: Notify API
# ══════════════════════════════════════════════

def notify_api(output_file_path, category, reencoded_directory):
    """
    Sends appropriate API request based on category (Shows/Movies).
    """
    api_config = API_MAPPING.get(category)
    if not api_config:
        logger.error(f"Unknown category: {category}. Skipping API call.")
        return

    json_payload = {"name": api_config["command"], "path": output_file_path}
    
    try:
        response = requests.post(
            api_config["url"],
            headers={"X-Api-Key": api_config["api_key"]},
            json=json_payload
        )
        response.raise_for_status()
        logger.info(f"{category} API Response: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Failed to contact {category} API: {e}")
        return

    time.sleep(API_DELAY_TIME)

    if not os.path.exists(output_file_path):
        logger.info(f"File was imported by {category} API: {output_file_path}")
        # Clean up empty directory if file was imported
        if not os.listdir(reencoded_directory):
            os.rmdir(reencoded_directory)
            logger.info(f"Cleaned up empty directory: {reencoded_directory}")
    else:
        logger.warning(f"File was NOT imported by {category} API: {output_file_path}")

# ══════════════════════════════════════════════
# 🚀 SECTION 9: Main Program
# ══════════════════════════════════════════════

def main():
    """
    Entry point: reads file list with categories, probes metadata, and processes matches.
    """
    logger.info("========== Unified Media Processing Script Started ==========")

    if not os.path.exists(TEXT_FILE_PATH):
        logger.error(f"Text file not found: {TEXT_FILE_PATH}")
        return

    with open(TEXT_FILE_PATH, 'r') as file:
        lines = [line.strip().strip('"') for line in file if line.strip()]

    if len(lines) % 2 != 0:
        logger.error("The number of lines in the text file should be even (file path followed by category).")
        return

    for i in range(0, len(lines), 2):
        file_path = lines[i]
        category = lines[i + 1]

        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue

        codec, width = get_video_info(file_path)
        if codec is None or width is None:
            logger.warning(f"Skipping file due to missing metadata: {file_path}")
            continue

        process_media_info(file_path, codec, width, category)

    logger.info("========== Unified Media Processing Script Finished ==========")

# ══════════════════════════════════════════════
# 🧷 Entry Point
# ══════════════════════════════════════════════

if __name__ == "__main__":
    main()
