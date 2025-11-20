@echo off
echo ========================================
echo    Building VidsDL v2.1 - Simple Build
echo ========================================
echo.

REM Install dependencies if needed
pip install pyinstaller pywebview flask flask-cors yt-dlp --quiet

echo.
echo Building single executable (this takes longer but works better)...
echo.

REM Simple onefile build - let PyInstaller handle everything
pyinstaller --noconfirm --onefile --windowed ^
    --name "VidsDL" ^
    --add-data "localindex.html;." ^
    --collect-all yt_dlp ^
    app-clean-FINAL.py

echo.
echo ========================================
echo Build complete!
echo.
echo Executable: dist\VidsDL.exe
echo Downloads will be in: dist\_MEI*\downloads\
echo (temporary folder created when running)
echo ========================================
echo.
pause
