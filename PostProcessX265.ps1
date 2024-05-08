<# Script variables for system customization.
PathtoOutputDirectory - Change this varible to set the output directory.
HandBrakeCLI - Change this variable to reflect the path to the HandBrakeCLI.exe on your system, or leave as is if you have added that path to the PATH Systen Variable.
#>

# Define the parameter for the source directory
[CmdletBinding()]
param (
    [Parameter(Mandatory=$True,ValueFromPipeline=$True,Position=0)]
    [ValidateScript({ForEach($item in $_){Test-Path $_}})]
    [string] $sourceDir
)


<#  Retired as redundant - JG 05042024

    - Check if the source directory is provided 
    if (-not $sourceDir) {
        Write-Host "Please provide the source directory by dragging and dropping a folder onto this script."
        exit
    }
#>




<#  Multiple modifications to extensions list - JG 05042024 
    
    Removed Wildcards, which are not needed for filter, improves run speed.
    
    Joined list into string for use in regex filter for files. This
    facilitates using a single search for all files moving iterative
    load from n4 to n0
#>

# Specify the video file extensions to search for
$videoExtensions = @('.mp4', '.mkv', '.avi', '.mov', '.wmv') -join "|"


<#  Retired as no need to instantiate variables ahead of use. -JG 05042024

    Only need to do this if you need an empty list or object to add elements to.
    i.e. $myList = @()
         $myObject = @{}
    
    - Initialize variables to store information about the largest video file
    $largestVideoFile = $null
    $largestSize = 0

    
#>


# Better Method to iterate through files
$videoFiles = Get-ChildItem -Path $sourceDir | Where-Object {$_.Extension -match $videoExtensions}

# Loop through each video file extension <--- Does this need to be a recursive search (all subfolders)?
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
exit($Error)
