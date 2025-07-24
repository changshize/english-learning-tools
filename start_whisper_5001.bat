@echo off
echo Starting Whisper Server 2 (Port 5001)
echo ========================================

if not exist "whisper_isolated" (
    echo ERROR: Isolated environment does not exist
    echo Please run: create_isolated_env.bat first
    pause
    exit /b 1
)

echo Activating isolated environment...
call whisper_isolated\Scripts\activate.bat

echo Starting Whisper Server on port 5001...
python faster_whisper_server.py 5001

pause
