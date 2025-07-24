@echo off
echo Starting Whisper Server 4 (Port 5003)
echo ========================================

if not exist "whisper_isolated" (
    echo ERROR: Isolated environment does not exist
    echo Please run: create_isolated_env.bat first
    pause
    exit /b 1
)

echo Activating isolated environment...
call whisper_isolated\Scripts\activate.bat

echo Starting Whisper Server on port 5003...
python faster_whisper_server.py 5003

pause
