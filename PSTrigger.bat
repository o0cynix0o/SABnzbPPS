@echo off

REM change EncodingPSScriptPath to the Complete "path\PSScriptToCall.ps1" of the postprocessing script with this.

REM Check if a folder was dropped onto the batch file
if "%~1" == "" (
    echo Please drag and drop a folder onto this batch file.
    pause
    exit /b
)

REM Run the PowerShell script with the dropped folder as a parameter
powershell.exe -ExecutionPolicy Bypass -File "EncodingPSScriptPath" "%~1"

pause
