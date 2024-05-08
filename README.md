# SABnzb PostProcessing Script for Handbrake Reencodes to x265

A PostProcessing Script written in Powershell to use Handbreak to ReEncode videos into x265.

## Description

During a mundane commute to work, a curious thought struck my mind: could ChatGPT lend its prowess to craft a script tailored for the postprocessing of downloads via SABNZB? Specifically, the aim was to encode them to the efficient x265 format, excise certain tracks and subtitles, and further compress the files. Which then turned into a learning project, when it comes down to it; I'd realyy like to know how its doing what its doing.

## Getting Started

### Dependencies

1. *HandBreak for Windows* - Download and install from main site. (https://handbrake.fr/downloads.php)
2. *HandbrakeCLI* - Download and extract .exe to your HandBreak directory. (https://handbrake.fr/downloads2.php)
3. *FFPROBE* - Download and extract .exe to your HandBreak directory. (https://ffmpeg.org/download.html)

### Installing

* Download and install from the HandBreak Links that have been provided. Remember where you are install HandBreak, and the other two EXE's. Put these all in the same folder (C:\Program  Files\HandBrake). You are going to need this path for the "HandBrakeCLI" variable inside of the script. Or you can add this path to the Windows System Variable "PATH" and you won't need this at all.
* You also need an output directory. This is set inside the script using the "PathtoOutputDirectory" variable inside the "PostProcessX265" script. This is manditory, the script will not work without it.
* You will also need the path to the PostProcessX265.ps1 script downloaded as part of this project. This path get added to the workflow by using the "EncodingPSScriptPath" variable inside of the "PSTrigger" batch file. 

### Executing program

* The PowerShell (PostProcessX265.ps1) is called by the batch script (PSTrigger.bat) this done by adding it under the "Script" option on the catagoy setup page inside of SABnzb located here: (http://127.0.0.1:YOURPORTGOESHERE/sabnzbd/config/categories/)

* Or you can drag a folder or video file on to the batch script (PSTrigger.bat) and it should trigger automaticly. 

## Help

* Google is your friend.

## Authors

* o0cYN1X0o - Padawan
* GoyerGeek - Jedi Master
* ChatGPT - Confused, "Go home you're drunk."

## Version History

* Nothin' to see here...move along....

## License

This project is licensed under GNU General Public License v3.0 - see the LICENSE.md file for details

## Acknowledgments

Terry Hoitz - "Fly peacock, fly!"