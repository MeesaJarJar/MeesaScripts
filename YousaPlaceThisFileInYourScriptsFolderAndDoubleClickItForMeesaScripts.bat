@echo off
setlocal enabledelayedexpansion

REM Define variables
set repo_url=https://github.com/MeesaJarJar/MeesaScripts/archive/refs/heads/main.zip
set zip_file=MeesaScripts.zip
set extract_dir=MeesaScripts-main

REM Change to the directory where the scripts are stored
cd /d %~dp0

REM Download the repository ZIP file
echo Downloading repository...
powershell -command "Invoke-WebRequest -Uri '%repo_url%' -OutFile '%zip_file%'"

REM Check if download was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to download the repository ZIP file.
    pause
    exit /b 1
)

REM Extract the ZIP file
echo Extracting repository...
powershell -command "Expand-Archive -Path '%zip_file%' -DestinationPath . -Force"

REM Check if extraction was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to extract the repository ZIP file.
    pause
    exit /b 1
)

REM Copy files to the current directory
echo Updating scripts...
xcopy "%extract_dir%\*" "%~dp0" /s /e /y

REM Clean up
echo Cleaning up...
del /f /q %zip_file%
rd /s /q %extract_dir%

echo Update complete.
endlocal
