@echo off
setlocal

REM Get the full path to the directory containing the script
set "ScriptDir=%~dp0"

REM Create or clear the text file for storing video file paths
type nul > "%ScriptDir%TXT\FilesToBeProcessed.txt"

REM Expect: %1 = path, %2 = category (from qBittorrent %F and %L)
if "%~1"=="" goto done
if "%~2"=="" (
    echo ERROR: Category not provided.>&2
    exit /b 1
)
set "current=%~1"
set "category=%~2"

REM Check if the parameter is a directory or file
if exist "%current%\" (
    REM It's a directory, process all supported video files in the directory recursively
    for /R "%current%" %%F in (*.mp4 *.mkv *.mpg *.mpeg *.avi *.webm *.divx *.m2ts *.iso *.m4v *.ts) do (
        echo "%%F" >> "%ScriptDir%TXT\FilesToBeProcessed.txt"
        echo "%category%" >> "%ScriptDir%TXT\FilesToBeProcessed.txt"
    )
) else (
    REM It's a file, process the file if it matches supported extensions
    echo "%current%" >> "%ScriptDir%TXT\FilesToBeProcessed.txt"
    echo "%category%" >> "%ScriptDir%TXT\FilesToBeProcessed.txt"
)

:done
REM Call the Python script using the dynamic directory path to process the video files
python "%ScriptDir%Torrents.py"
exit
