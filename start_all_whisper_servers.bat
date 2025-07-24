@echo off
echo Starting All Whisper Servers (4 instances)
echo ============================================
echo This will open 4 command windows for Whisper servers
echo Ports: 5000, 5001, 5002, 5003
echo.
echo Press any key to start all servers...
pause >nul

echo Starting Whisper Server 1 (Port 5000)...
start "Whisper Server 5000" start_whisper_5000.bat

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo Starting Whisper Server 2 (Port 5001)...
start "Whisper Server 5001" start_whisper_5001.bat

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo Starting Whisper Server 3 (Port 5002)...
start "Whisper Server 5002" start_whisper_5002.bat

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo Starting Whisper Server 4 (Port 5003)...
start "Whisper Server 5003" start_whisper_5003.bat

echo.
echo SUCCESS: All 4 Whisper servers are starting!
echo.
echo Server URLs:
echo - http://localhost:5000
echo - http://localhost:5001
echo - http://localhost:5002
echo - http://localhost:5003
echo.
echo You can now run the parallel subtitle processor
echo.
pause
