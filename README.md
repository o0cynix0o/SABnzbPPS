This project came out of a random thought on the way to work one day. "Can I use ChatGPT to write a script for postprocessing my downloads with SABNZB to encode them to x265 and strip out certain tracks and subtitles and also compress the files as well?"
you need a few things installed in order for this to wiork.
Handbreak for Windows
HandbreakCLI for Windows
And FFPROBE also in the handbreak dir==During a mundane commute, a curious thought struck my mind: could ChatGPT lend its prowess to craft a script tailored for the postprocessing of downloads via SABNZB? Specifically, the aim was to encode them to the efficient x265 format, excise certain tracks and subtitles, and further compress the files. However, to embark on this endeavor, several prerequisites must be fulfilled:

1. **Handbrake for Windows**: This indispensable tool facilitates the transcoding process.
2. **HandbrakeCLI for Windows**: The Command Line Interface (CLI) variant of Handbrake, essential for script automation.
3. **FFPROBE**: A critical component, residing within the Handbrake installation directory, indispensable for probing multimedia files.

Before diving into the script, it's imperative to ensure Handbrake is installed correctly, and HandbrakeCLI is downloaded and extracted to the Handbrake installation directory. To streamline command execution, consider appending this directory to the PATH Environment Variable in Windows.

With these prerequisites in place, the script can seamlessly orchestrate the postprocessing workflow, transforming downloads into optimized x265-encoded files, selectively stripping undesired tracks and subtitles, and applying compression for efficient storage and distribution.
you need to install handbreak and download and extract HandbreakCLI to the Handbreak install DIR. You need to either add this path to the PATH Environment Varible in Windows, so the cammands will run as expected.
