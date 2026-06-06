@echo off
set SERVER=root@45.192.97.233
set PORT=22
set PASS=K4NHWFAPDGsX

echo Creating deployment directory...
echo mkdir -p /var/www/quiz-system > deploy_commands.txt
echo cd /var/www/quiz-system >> deploy_commands.txt
echo rm -rf * >> deploy_commands.txt
echo git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git . >> deploy_commands.txt
echo cd /var/www/quiz-system/backend >> deploy_commands.txt
echo pip3 install -r requirements.txt >> deploy_commands.txt
echo pip3 install flask flask-cors pymysql sqlalchemy python-dotenv xlsxwriter >> deploy_commands.txt
echo cd /var/www/quiz-system/frontend >> deploy_commands.txt
echo npm install >> deploy_commands.txt
echo npm run build >> deploy_commands.txt
echo systemctl restart nginx >> deploy_commands.txt
echo pm2 restart all >> deploy_commands.txt
echo Deployment completed!

echo.
echo Using SSH with password via stdin...

(
echo mkdir -p /var/www/quiz-system
echo cd /var/www/quiz-system
echo rm -rf *
echo git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
echo ls -la
) | plink -batch -P %PORT% %SERVER% %PASS% 2>&1

pause
