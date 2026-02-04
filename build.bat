@echo off
REM eq_resist_overlay.bat - Build script for creating executable

echo Installing/ensuring PyInstaller is available...
pip install pyinstaller --quiet --upgrade

echo.
echo Building executable...

python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "EQ_Resist_Overlay" ^
    --icon=NONE ^
    --add-data "%~dp0npc_types.sql;." ^
    --distpath dist ^
    --workpath build ^
    --specpath build ^
    --clean ^
    eq_resist_overlay.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build FAILED! Check the output above for errors.
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Build complete!
echo.
echo Output should be here: dist\EQ_Resist_Overlay.exe
echo.
pause