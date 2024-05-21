@echo off

REM Variables:
REM %SCRIPT_FOLDER% - Path to the folder containing the PowerShell script.

REM Set the path to the folder containing the PowerShell script
set "SCRIPT_FOLDER=G:\Scripts\Encoders"

REM Check if a folder was dropped onto the batch file
if "%~1" == "" (
    echo Please drag and drop a folder onto this batch file.
    pause
    exit /b
)

REM Run the MovieENC PowerShell script with the dropped folder as a parameter
powershell.exe -ExecutionPolicy Bypass -File "%SCRIPT_FOLDER%\MovieENC - 4K.ps1" "%~1"
