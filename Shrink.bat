@echo off
setlocal

REM Get the full path to the directory containing the script
set "ScriptDir=%~dp0"

REM Create or clear the text file
type nul > "%ScriptDir%TXT\FilesToBeProcessed_v2.txt"

REM Loop through each argument passed to the batch file
:next
if "%~1"=="" goto done
set "current=%~1"

REM Check if the parameter is a directory or file
if exist "%current%\" (
    REM It's a directory, process all supported video files in the directory recursively
    for /R "%current%" %%F in (*.mp4 *.mkv *.mpg *.mpeg *.avi *.webm *.divx *.m2ts *.iso *.m4v) do (
        echo "%%F" >> "%ScriptDir%TXT\FilesToBeProcessed_v2.txt"
    )
) else (
    REM It's a file, process the file if it matches supported extensions
    echo "%current%" >> "%ScriptDir%TXT\FilesToBeProcessed_v2.txt"
)

REM Shift to the next argument
shift
goto next

:done
REM Call the PowerShell script using the dynamic directory path
python %ScriptDir%Shrink.py
exit
