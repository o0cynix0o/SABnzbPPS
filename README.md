# SABnzb PostProcessing Script for Handbrake Reencodes to x265

A PostProcessing Script written in Python to use HandBrake to reencode videos into x265 format.

## Description

During a mundane commute to work, an intriguing notion dawned on me: could ChatGPT wield its prowess to craft a script tailored for the post-processing of downloads via SABNZB? Specifically, the aim was to encode them into the efficient x265 format, excise certain tracks and subtitles, and further compress the files. This sparked a determined curiosity within me, driving a quest to understand the mechanics behind this endeavor and delve into its inner workings.

## Getting Started

### Installing Dependencies

1. **Download the project as a zip from GitHub**:
   - Go to the [GitHub project page](https://github.com/o0cynix0o/SABnzbPPS).
   - Click on the "Code" button and select **Download ZIP**.
2. After downloading and extracting the ZIP, locate the **App** folder inside the extracted project files.
3. **Download and place the required executables**:
   - **HandBrakeCLI.exe**: Download it from [HandBrake CLI Download Page](https://handbrake.fr/downloads2.php).
   - **FFprobe.exe**: Download it from [FFmpeg Download Page](https://ffmpeg.org/download.html).
   - Place both executables inside the **App** folder. These executables are required for the script to function.
4. You don't need to install HandBrake for Windows, but you may choose to install it if you want to adjust or view preset settings using the HandBrake GUI. You can download it from the [HandBrake for Windows page](https://handbrake.fr/downloads.php).
5. The **Presets** folder inside the project includes the required HandBrake presets for processing video files. You can modify these presets if needed by importing them into HandBrake's GUI application.
6. The **ReEncodedFiles** directory is included in the zip and is set as the default output directory for processed files. This output directory will be used automatically for storing reencoded media files.

### Creating Categories for Downloaders

#### **qBittorrent**:

1. Open **qBittorrent** and go to **Tools > Options**.
2. Navigate to the **Downloads** section.
3. Under **Run external program on torrent completion**, enable the option by checking the box.
4. In the **Run external program** field, input the following command, replacing `"C:\path\to\project\Torrents.bat"` with the actual path where your **Torrents.bat** is located:
   ```plaintext
   "C:\path\to\project\Torrents.bat" "%F" "%L"
   ```
   - `%F` is the file path.
   - `%L` is the category (e.g., "Movies" or "TVShow").
5. Save the changes and restart qBittorrent.
6. Create categories to match the scripts by doing the following:
   - Go to **Tools > Options > Downloads**.
   - Under **Categories**, add categories like **Movies** and **TVShow** to correspond with the `Movies.bat` and `TVShows.bat` scripts.
7. Once set up, qBittorrent will call **Torrents.bat** with the appropriate category when the download completes, passing the category and file path to the corresponding script.

#### **SABnzbd**:

1. Open **SABnzbd** and go to **Config**.
2. Navigate to the **Categories** section.
3. Create categories like **Movies** and **TVShow**.
   - For each category, set the corresponding **Post-Processing Script** to the batch file associated with the category.
     - For **Movies**, set the Post-Processing Script to **Movies.bat**.
     - For **TV Shows**, set the Post-Processing Script to **TVShows.bat**.
4. When SABnzbd completes a download, it will automatically run the relevant `.bat` file, which triggers the Python scripts to process the downloaded file.
   - Ensure that the **Movies.bat** and **TVShows.bat** files are correctly pointing to the scripts to process the respective files.

### Execution

* **qBittorrent**:
   1. Set up the **Torrents.bat** file to run after downloading a torrent by configuring the **Run External Program** setting under **Tools > Options > Downloads**.
   2. In the **Run external program** field, set the path to **Torrents.bat** and pass the following parameters:
      ```plaintext
      "C:\path\to\project\Torrents.bat" "%F" "%L"
      ```
      Where `%F` is the file path and `%L` is the category of the torrent (e.g., "Movies" or "TVShow").
   3. The script will automatically detect the category (Movies or TV Shows) and call the appropriate batch file to process the video.

* **SABnzbd**:
   1. Add the **Movies.bat** or **TVShow.bat** script as post-processing triggers in your SABnzbd categories.
   2. When a file is downloaded, it will trigger the appropriate batch file, reencode the file, and organize it into the designated output directory (**ReEncodedFiles**).

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

Simply extract the project ZIP, download the required executables, and place them in the **App** folder. No additional setup is required for the folder structure. To reencode a single file, simply drag and drop the file onto the corresponding `.bat` file.
