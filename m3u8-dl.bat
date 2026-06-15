@echo off
title M3U8 Video Downloader for Windows
color 0A

echo ========================================
echo    🎥 M3U8 Video Downloader (Windows)
echo ========================================
echo.

:: Check for ffmpeg
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ffmpeg not found!
    echo.
    echo Install ffmpeg:
    echo 1. Download: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to PATH
    pause
    exit /b 1
)

set /p "url=Enter M3U8 URL: "
if "%url%"=="" (
    echo No URL provided!
    pause
    exit /b 1
)

set /p "filename=Output filename (press Enter for auto): "
if "%filename%"=="" (
    set filename=m3u8_video_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set filename=%filename: =0%.mp4
)

echo.
echo Downloading...
ffmpeg -i "%url%" -c copy -bsf:a aac_adtstoasc -y "%filename%"

if exist "%filename%" (
    echo.
    echo ========================================
    echo    Download Complete! %filename%
    echo ========================================
) else (
    echo Download failed!
)
pause
