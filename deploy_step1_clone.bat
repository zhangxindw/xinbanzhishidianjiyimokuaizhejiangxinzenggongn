@echo off
echo ========================================
echo Step 1: Cloning repository from GitHub
echo ========================================
"D:\putty\plink.exe" -ssh root@154.201.94.140 -pw 6dwic8N532a7 -P 22 -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" "cd /var/www && rm -rf quiz-system 2>/dev/null; git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuaizhejiangxinzenggongn.git quiz-system"
echo.
echo Step 1 completed!
pause
