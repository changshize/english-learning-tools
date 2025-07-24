@echo off
echo Starting Multiple Whisper Servers
echo ==================================

start "Whisper 5000" start_whisper_5000.bat
timeout /t 3 /nobreak >nul

start "Whisper 5001" start_whisper_5001.bat  
timeout /t 3 /nobreak >nul

start "Whisper 5002" start_whisper_5002.bat
timeout /t 3 /nobreak >nul

start "Whisper 5003" start_whisper_5003.bat

echo SUCCESS: All servers starting
echo Check: http://localhost:5000/health
echo Check: http://localhost:5001/health  
echo Check: http://localhost:5002/health
echo Check: http://localhost:5003/health
pause
