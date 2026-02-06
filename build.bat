@echo off
REM build.bat - One-step release builder (EXE + DB + zip)

setlocal
set OUTDIR=release

echo Building release zip...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_release.ps1" -OutDir %OUTDIR%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Release build FAILED! Check the output above for errors.
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Release build complete. See: %OUTDIR%\
endlocal