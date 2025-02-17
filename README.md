# PostProcessing Script for HandBrake Reencodes to x265  

A PostProcessing Script written in Python to use HandBrake to reencode videos into x265 format.  

## Description  

This project is a PostProcessing Script written in Python designed to reencode your media into the efficient x265 format, remove certain audio tracks and subtitles, and save space. The scripts are the result of months of work and testing, and I hope they help others streamline their media management.  

### How It Works  

1. **Download Client Integration**:  
   - When a download completes, the download client (such as qBittorrent or SABnzbd) passes the file category and file path to the appropriate batch file (**Movies.bat**, **TVShows.bat**, or **Torrents.bat**).  
   - The batch file creates a text file in the **TXT** folder containing the category and file path information and triggers the corresponding Python script (**Movies.py**, **TVShows.py**, or **Torrents.py**).  

2. **File Scanning**:  
   - The Python script scans the file using **FFprobe**, extracting information about the codec and resolution of the video.  

3. **Preset Selection**:  
   - Based on the video's resolution, the script selects the appropriate HandBrake preset for reencoding:  
     - Files with a width of **1920 pixels or less** are processed using the **HD** preset.  
     - Files with a width between **1921 and 3840 pixels** are processed using the **4K** preset.  

4. **Reencoding Process**:  
   - The video is reencoded using HandBrakeCLI with the selected preset. The reencoded file is saved to the **ReEncodedFiles** directory.  

5. **API Calls for Further Processing**:  
   - After the reencoding is complete, an API call is made depending on the script used:  
     - For **NZB** downloads (handled by **Movies.py** and **TVShows.py**), the corresponding service (**Radarr** for movies or **Sonarr** for TV shows) receives the API call to process the reencoded file.  
     - For **Torrents** (handled by **Torrents.py**), the service is determined by the category passed to the **Torrents.bat** file.  
   - The respective service processes the request, and the reencoded file is moved or removed from the **ReEncodedFiles** directory accordingly.  

### **Manual Reencoding Mode**  

A standalone version of the script, **Shrink.py**, is now included for manually shrinking files as needed, without making API calls. This allows users to reencode files on demand without affecting automation processes. To use this version, simply drag and drop the file onto **Shrink.bat**, and the script will handle the reencoding without interfacing with external services. Or using the "Right Click, Send To" method layed out in the project wiki.

This workflow ensures a smooth and automated reencoding and management process for your media files, maximizing storage efficiency and compatibility with various playback devices.  

Go to the [GitHub Wiki page](https://github.com/o0cynix0o/SABnzbPPS/wiki) for install and setup instructions.  

## Notes  

Simply extract the latest release, no additional setup is required for the folder structure. To reencode a single file, simply drag and drop the file onto the corresponding `.bat` file.  

## Help  

Google is your friend.  

## Authors  

- **o0cYN1X0o** - Padawan  
- **GoyerGeek** - Jedi Master  
- **ChatGPT** - Confused, "Go home you're drunk."  

## Version History  

Nothin' to see here... move along....  

## License  

This project is licensed under GNU General Public License v3.0 - see the LICENSE.md file for details.  

## Acknowledgments  

*"I am a peacock, you gotta let me fly!" - Terry Hoitz*  
