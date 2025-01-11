# PostProcessing Script for Handbrake Reencodes to x265

A PostProcessing Script written in Python to use HandBrake to reencode videos into x265 format.

## Description

The aim is to reencode your media into the efficient x265 format, excise certain audio tracks and subtitles, to save space. These scripts are the result of months of work and testing. I hope they help. If you have any suggestions, please feel free to let me know.

## Getting Started

### Installing Dependencies

1. **Download the project as a zip from GitHub**:
   - Go to the [GitHub project page](https://github.com/o0cynix0o/SABnzbPPS).
   - Click on the "Code" button and select **Download ZIP**.
   
2. After downloading and extracting the ZIP, locate the **App** folder inside the extracted project files.

3. **Download and place the required executables**:
   - **HandBrakeCLI.exe**: Download from the [HandBrake CLI Download Page](https://handbrake.fr/downloads2.php).
   - **FFprobe.exe**: Download from the [FFmpeg Download Page](https://ffmpeg.org/download.html).
   - Place both executables inside the **/SABnzbPPS/App** folder.

4. You don't need to install HandBrake for Windows, but you may choose to install it if you want to adjust or view preset settings using the HandBrake GUI. You can download it from the [HandBrake for Windows page](https://handbrake.fr/downloads.php).

5. The **Presets** folder inside the project includes the required HandBrake presets for processing video files. You can modify these presets if needed by importing them into HandBrake's GUI application.

6. The **ReEncodedFiles** directory is included in the zip and is set as the default output directory for processed files. This output directory will be used automatically for storing reencoded media files.

### Setting up scripts for action

The scripts require API keys to interact with their respective services Sonarr for TVShows, Radarr for Movies. Here’s how you can find and set the API keys in the corresponding Python scripts:

1. **Find Your API Key**:
   - **Sonarr**:
     1. Go to your Sonarr instance, usually located at `http://localhost:8989` (or the address and port you configured).
     2. In Sonarr, navigate to **Settings > General > Security**.
     3. Find your **API Key** under the **Security** section.

   - **Radarr**:
     1. Go to your Radarr instance, usually located at `http://localhost:7878` (or the address and port you configured).
     2. In Radarr, navigate to **Settings > General > Security**.
     3. Find your **API Key** under the **Security** section.

2. **Set Your API Key in the Python Scripts**:
   - Open the relevant Python script (`Movies.py` for Radarr, `TVShows.py` for Sonarr, or `Torrents.py` for your torrent client).
   - Find the following lines in each script:
     ```python
     sonarr_api_key = "YOUR_SONARR_API_KEY"
     radarr_api_key = "YOUR_RADARR_API_KEY"
     ```
   - Replace `"YOUR_SONARR_API_KEY"` with the API key you found for Sonarr, in scripts TVShows.py and Torrnets.py. and replace `"YOUR_RADARR_API_KEY"` with the API key you found for Radarr in scripts Movies.py, and Torrnets.py.
   - Save the changes to each script.

With these steps, your scripts will be properly connected to Sonarr, Radarr, allowing for seamless post-processing of movies, TV shows, and torrents.

### Setting up Donaloaders to work with the Batch files

#### **qBittorrent**:

1. Create categories to match the scripts by doing the following**:
   - Go to **Tools > Options > Downloads**.
   - Under **Categories**, add categories **Movies** and **TVShows**. **These precise category names need to be used** as that's what the script is expecting.
2. Set up the **Torrents.bat** file to run after downloading a torrent by configuring the **Run External Program** setting under **Tools > Options > Downloads**.
   - In the **Run external program** field, set the path to **Torrents.bat** and pass the following parameters:
      ```plaintext
      "C:\path\to\project\Torrents.bat" "%F" "%L"
      ```
      Where `%F` is the file path and `%L` is the category of the torrent (e.g., "Movies" or "TVShow").
  
    
Once set up, qBittorrent will pass the file path and category to **Torrents.bat**. The batch will create a file called **FilesToBeReencoded.txt** in the **TXT** folder and then trigger **Torrents.py** to process the file.

#### **SABnzbd**:

1. Open **SABnzbd** and go to **Config**.
2. Navigate to the **Categories** section.
3. Create categories like **Movies** and **TVShow**.
   - For each category, set the corresponding **Post-Processing Script** to the batch file associated with the category.
     - For **Movies**, set the Post-Processing Script to **Movies.bat**.
     - For **TV Shows**, set the Post-Processing Script to **TVShows.bat**.
4. When SABnzbd completes a download, it will automatically run the relevant `.bat` file, which triggers the Python scripts to process the downloaded file.
   - Ensure that the **Movies** and **TVShows** catagories are correctly pointing to the correct .bat files to process the respective media types.

### Setting Up and Manually Processing Files Using Right-Click "Send To" Menu

You can easily trigger the batch scripts (Movies.bat or TVShows.bat) from the Windows right-click context menu using the **Send To** option. Follow these steps to set it up:

1. **Create Shortcuts for the Batch Scripts**:
   - First, create shortcuts for the batch scripts that correspond to the types of media you want to process:
     - **Movies.bat**: For processing movie files.
     - **TVShows.bat**: For processing TV show files.
   - Right-click on the **Movies.bat** file in your project directory and select **Create Shortcut**. Do the same for **TVShows.bat**.
   - After creating the shortcuts, **rename** the shortcuts to `Movies` and `TVShows` to match the category names expected by the script.
   - Move the renamed shortcuts to the **SendTo** folder. You can find the **SendTo** folder by pressing `Win + R` to open the Run dialog, then typing `shell:SendTo` and pressing Enter. This will open the folder containing the "Send To" shortcuts.

2. **Using the Right-Click "Send To" Menu**:
   - After completing the setup, you can right-click on any video file (either a movie or a TV show) in Windows Explorer.
   - Choose **Send To**, then select either **Movies** or **TVShows** to trigger the corresponding script.
   - The selected script will then run, reencoding the file and placing it in the designated output directory (**ReEncodedFiles**).

### Folder Structure

The folder structure is maintained automatically when you download the project as a ZIP from GitHub. Here's what it will look like after extraction (Not including the .exe files):

```
Project Directory (SABnzbPPS)
│
├── App/                        (HandBrakeCLI.exe and FFprobe.exe go here)
│   └── HandBrakeCLI.exe        (Used by the script to reencode videos)
│   └── FFPROBE.exe             (Used by the script to scan video files for resolution)
├── Presets/                    (HandBrake preset files go here)
│   └── SuperShrink4K.json      (4K preset used by HandBrakeCLI)
│   └── SuperShrinkHD.json      (HD preset used by HandBrakeCLI)
├── ReEncodedFiles/             (Processed media files will be saved here)
├── TXT/                        (Files used by the Python scripts to find the category and file path for the downloaded file)
│   └── FilesToBeProcessed.txt  (List of files to be processed by the Torrents.py script)
│   └── ShowsToBeProcessed.txt  (List of files to be processed by the TVShows.py script)
│   └── MoviesToBeProcessed.txt (List of files to be processed by the Movies.py script)
├── Movies.bat                  (Batch script for movie processing, passing file path and category to Python script)
├── TVShows.bat                 (Batch script for TV show processing, passing file path and category to Python script)
├── Torrents.bat                (Batch script for torrent processing, passing file path and category to Python script)
└── TVShows.py                  (Main Python TV Show processing script)
└── Movies.py                   (Main Python Movie processing script)
└── Torrents.py                 (Main Python Torrent processing script)
```

## Notes

Simply extract the project ZIP, download the required executables, and place them in the **App** folder. No additional setup is required for the folder structure. To reencode a single file, simply drag and drop the file onto the corresponding `.bat` file.

## Help

Google is your friend.

## Authors

* o0cYN1X0o - Padawan
* GoyerGeek - Jedi Master
* ChatGPT - Confused, "Go home you're drunk."

## Version History

Nothin' to see here...move along....

## License

This project is licensed under GNU General Public License v3.0 - see the LICENSE.md file for details

## Acknowledgments

*Terry Hoitz - "Fly peacock, fly!"
