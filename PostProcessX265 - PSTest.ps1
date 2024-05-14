<# Script variables for system customization.
PathtoOutputDirectory - Change this variable to set the output directory.
HandBrakeCLI - Change this variable to reflect the path to the HandBrakeCLI.exe on your system, or leave as is if you have added that path to the PATH System Variable.
LogFilePath - Change this variable to set the path for the log file where all output will be recorded.
#>

# Define the parameter for the source directory
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True,ValueFromPipeline=$True,Position=0)]
    [ValidateScript({ForEach($item in $_){Test-Path $_}})]
    [string] $sourceDir
)

# Specify the video file extensions to search for
$videoExtensions = @('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.iso', '.webm') -join "|"

# Initialize variables to track the largest video file
$largestVideoFile = $null
$largestSize = 0

# Better Method to iterate through files
$videoFiles = Get-ChildItem -Path $sourceDir -Recurse -File | Where-Object {$_.Extension -match $videoExtensions}

# Loop through each video file to find the largest one
foreach ($file in $videoFiles) {
    $fileSize = $file.Length
    if ($fileSize -gt $largestSize) {
        $largestSize = $fileSize
        $largestVideoFile = $file.FullName
    }
}

# Output the name of the largest video file
if (-not $largestVideoFile) {
    Write-Host "No video files found in the specified directory."
    exit
}

# Specify the output directory for the converted files
$outputDir = "PathtoOutputDirectory"
if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force
}

# Construct the output file path for the converted video
$outputFileName = [System.IO.Path]::GetFileNameWithoutExtension($largestVideoFile) + ".mkv"
$outputFilePath = Join-Path -Path $outputDir -ChildPath $outputFileName

# Define the path for the log file
# Your log file path - change this to your desired location
$LogFilePath = "C:\Path\To\Your\Log\File\" + [System.IO.Path]::GetFileNameWithoutExtension($outputFileName) + ".log"

# Redirect all output to the log file
Start-Transcript -Path $LogFilePath -Append

# Display a message indicating the start of the conversion process
Write-Host "Processing video file: $largestVideoFile"

# Start HandBrakeCLI process to convert the video file to MKV format
$HandBrakeCLIPath = "HandBrakeCLI" # Change this if the path is different or not in PATH
$handBrakeArgs = "-i `"$largestVideoFile`" -o `"$outputFilePath`" --preset-import-gui --verbose=1"
Start-Process -FilePath $HandBrakeCLIPath -ArgumentList $handBrakeArgs -NoNewWindow -Wait

# Display a message indicating the completion of the conversion process
Write-Host "Conversion complete. Output file: $outputFilePath"

# Stop the transcript to end logging
Stop-Transcript

# Close the PowerShell window
exit($Error)
