@echo off
echo Starting 8 Whisper Servers for Maximum Speed
echo ============================================
echo WARNING: This requires 16GB+ RAM and 8+ CPU cores
echo.

echo Starting servers...
start "Whisper 5000" start_whisper_5000.bat
timeout /t 2 /nobreak >nul

start "Whisper 5001" start_whisper_5001.bat  
timeout /t 2 /nobreak >nul

start "Whisper 5002" start_whisper_5002.bat
timeout /t 2 /nobreak >nul

start "Whisper 5003" start_whisper_5003.bat
timeout /t 2 /nobreak >nul

start "Whisper 5004" cmd /c "call whisper_isolated\Scripts\activate.bat && python faster_whisper_server.py 5004"
timeout /t 2 /nobreak >nul

start "Whisper 5005" cmd /c "call whisper_isolated\Scripts\activate.bat && python faster_whisper_server.py 5005"
timeout /t 2 /nobreak >nul

start "Whisper 5006" cmd /c "call whisper_isolated\Scripts\activate.bat && python faster_whisper_server.py 5006"
timeout /t 2 /nobreak >nul

start "Whisper 5007" cmd /c "call whisper_isolated\Scripts\activate.bat && python faster_whisper_server.py 5007"

echo.
echo SUCCESS: 8 Whisper servers starting
echo Ports: 5000-5007
echo.
echo Health checks:
echo http://localhost:5000/health
echo http://localhost:5001/health
echo http://localhost:5002/health
echo http://localhost:5003/health
echo http://localhost:5004/health
echo http://localhost:5005/health
echo http://localhost:5006/health
echo http://localhost:5007/health
echo.
pause
