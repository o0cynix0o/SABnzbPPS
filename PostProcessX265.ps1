# Script to convert the largest video file in a directory to MKV format using HandBrakeCLI
# PathtoOutputDirectory - Change this varible w/ (CTRL+H or the Find and Replace function) to set the outout directory.


# Define the parameter for the source directory
[CmdletBinding()]
param (
    [Parameter(Mandatory=$False,ValueFromPipeline=$True,Position=0)]
    [ValidateScript({ForEach($item in $_){Test-Path $_}})]
    [string] $sourceDir
)


<#
    - Check if the source directory is provided - 
    Deprecated and retired due to redundant check.
    Parameter block tests for path and exits if 
    does not exist.  

    if (-not $sourceDir) {
        Write-Host "Please provide the source directory by dragging and dropping a folder onto this script."
        exit
    }
#>

# Specify the video file extensions to search for
$videoExtensions = @('*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv')

# Initialize variables to store information about the largest video file
$largestVideoFile = $null
$largestSize = 0

# Loop through each video file extension
foreach ($ext in $videoExtensions) {
    # Get all video files with the current extension in the source directory
    $videoFiles = Get-ChildItem -Path $sourceDir -Filter $ext | Where-Object { $_.Length -gt 0 }
    
    # Loop through each video file to find the largest one
    foreach ($file in $videoFiles) {
        $fileSize = $file.Length
        if ($fileSize -gt $largestSize) {
            $largestSize = $fileSize
            $largestVideoFile = $file.FullName
        }
    }
}

# Output the name of the largest video file
if (-not $largestVideoFile) {
    Write-Host "No video files found in the specified directory."
    exit
}

# Specify the output directory for the converted files
$outputDir = "PathtoOutputDirectory"

# Construct the output file path for the converted video
$outputFileName = $largestVideoFile | Split-Path -Leaf
$outputFilePath = "$outputDir\$($outputFileName.Replace('.', '_')).mkv"

# Display a message indicating the start of the conversion process
Write-Host "Processing video file: $largestVideoFile"

# Start HandBrakeCLI process to convert the video file to MKV format
Start-Process -FilePath "HandBrakeCLI" -ArgumentList "-i `"$largestVideoFile`" -o `"$outputFilePath`" --preset-import-gui --verbose=1" -NoNewWindow -Wait

# Display a message indicating the completion of the conversion process
Write-Host "Conversion complete."

# Close the PowerShell window
exit
