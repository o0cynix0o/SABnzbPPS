# SABnzb PostProcessing Script for Handbrake Reencodes to x265

A PostProcessing Script written in Powershell to use Handbreak to ReEncode videos into x265.

## Description

During a mundane commute to work, a curious thought struck my mind: could ChatGPT lend its prowess to craft a script tailored for the postprocessing of downloads via SABNZB? Specifically, the aim was to encode them to the efficient x265 format, excise certain tracks and subtitles, and further compress the files. Which then turned into a learning project, when it comes down to it; I'd realyy like to know how its doing what its doing.

## Getting Started

### Dependencies

1. *HandBreak for Windows* - Download and install from main site. (https://handbrake.fr/downloads.php)
2. *HandbrakeCLI* - Download and extract .exe to your HandBreak install directory. (https://handbrake.fr/downloads2.php)
3. *FFPROBE* - Download and extract .exe to your HandBreak install directory. (https://ffmpeg.org/download.html)

### Installing

* You should know how to search out, download and install the HandBreak Links have been provided. Remember where you are going to install HandBreak, and the other two EXE's. Put these all in the same folder (C:\Program  Files\HandBrake). You are going to need this path for the "PathtoOutputDirectory" variable inside of the script. Or you can add this path to the Windows System Variable "PATH" and you won't need this at all.
* You also need an output directory. This is set inside the script using the "HandBrakeCLI" variable isside the script. This is manditory the script will not work without it.
* You will also need the path to the PostProcessX265.ps1 script downloaded as part of this project.

### Executing program

* The PowerShell (PostProcessX265.ps1) is called by the batch script (PSTrigger.bat) this done by adding it under the "Script" option on the catagoy setup page inside of SABnzb located here: (http://127.0.0.1:YOURPORTGOESHERE/sabnzbd/config/categories/)

* Or you can drag a folder or video file on to the batch script (PSTrigger.bat) and it should trigger automaticly. 

## Help

* Google is your friend.

## Authors

Contributors names and contact info

ex. o0cYN1X0o 
ex. 

## Version History

* Nothin' to see here...move along....

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)