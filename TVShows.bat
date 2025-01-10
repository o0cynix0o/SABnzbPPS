@echo off
setlocal

REM Batch Script to Prepare a List of Video Files for Processing
REM This script creates or clears a text file and populates it with the paths of video files
REM from the directories or files passed as arguments. It then calls a Python script for further processing.

REM Get the full path to the directory containing the script
set "ScriptDir=%~dp0"

REM Create or clear the text file where video file paths will be stored
type nul > "%ScriptDir%TXT\ShowsToBeProcessed.txt"

REM Loop through each argument passed to the batch file
:next
if "%~1"=="" goto done
set "current=%~1"

REM Check if the parameter is a directory or a file
if exist "%current%\" (
    REM If it's a directory, process all supported video files recursively
    for /R "%current%" %%F in (*.mp4 *.mkv *.mpg *.mpeg *.avi *.webm *.divx *.m2ts *.iso *.m4v) do (
        echo "%%F" >> "%ScriptDir%TXT\ShowsToBeProcessed.txt"
    )
) else (
    REM If it's a file, check if it has a supported extension and add to the text file
    echo "%current%" >> "%ScriptDir%TXT\ShowsToBeProcessed.txt"
)

REM Shift to the next argument
shift
goto next

:done
REM Call the Python script using the dynamic directory path
python %ScriptDir%TVShows.py
exit
