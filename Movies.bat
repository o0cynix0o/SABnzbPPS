@echo off
setlocal

REM Get the full path to the directory containing the script
set "ScriptDir=%~dp0"

REM Create or clear the text file for storing video file paths
type nul > "%ScriptDir%TXT\MoviesToBeProcessed.txt"

REM Loop through each argument passed to the batch file
:next
if "%~1"=="" goto done
set "current=%~1"

REM Check if the parameter is a directory or file
if exist "%current%\" (
    REM It's a directory, process all supported video files in the directory recursively
    for /R "%current%" %%F in (*.mp4 *.mkv *.mpg *.mpeg *.avi *.webm *.divx *.m2ts *.iso *.ts) do (
        echo "%%F" >> "%ScriptDir%TXT\MoviesToBeProcessed.txt"
    )
) else (
    REM It's a file, process the file if it matches supported extensions
    echo "%current%" >> "%ScriptDir%TXT\MoviesToBeProcessed.txt"
)

REM Shift to the next argument
shift
goto next

:done
REM Call the Python script using the dynamic directory path to process the video files
python "%ScriptDir%Movies.py"
exit
