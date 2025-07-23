@echo off
echo Starting Real Whisper AI Server (Isolated Environment)
echo ======================================================

if not exist "whisper_isolated" (
    echo ERROR: Isolated environment does not exist
    echo Please run: create_isolated_env.bat first
    pause
    exit /b 1
)

echo Activating isolated environment...
call whisper_isolated\Scripts\activate.bat

echo Checking Faster-Whisper...
python -c "from faster_whisper import WhisperModel; print('Faster-Whisper is ready!')"
if %errorlevel% neq 0 (
    echo ERROR: Faster-Whisper not working
    pause
    exit /b 1
)

echo.
echo Starting Real Whisper AI Server...
echo This will download the model on first use (about 244MB)
echo Server URL: http://localhost:5000
echo Health check: http://localhost:5000/health
echo Press Ctrl+C to stop server
echo.
python faster_whisper_server.py

pause
