@echo off
echo. | "D:\putty\plink.exe" -ssh root@154.201.94.140 -pw 6dwic8N532a7 -P 22 "cd /var/www/quiz-system && git pull origin main"