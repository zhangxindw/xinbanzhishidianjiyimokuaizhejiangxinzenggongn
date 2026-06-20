@echo off
echo ========================================
echo Updating SSH host key
echo ========================================
echo y | "D:\putty\plink.exe" -ssh root@154.201.94.140 -pw 6dwic8N532a7 -P 22 "echo Connection test"
echo.
echo Host key updated!
pause
