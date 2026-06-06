@echo off
chcp 65001 >nul
echo ========================================
echo 正在部署项目到服务器...
echo ========================================

set SERVER=45.192.97.233
set PORT=22
set USER=root
set PASS=K4NHWFAPDGsX

echo.
echo 第1步：创建远程目录并克隆代码...
plink -batch -P %PORT% %USER%@%SERVER% "mkdir -p /var/www/quiz-system && cd /var/www/quiz-system && rm -rf * && git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git ."

if %ERRORLEVEL% neq 0 (
    echo.
    echo 步骤1失败，尝试使用SSH命令...
    ssh -o StrictHostKeyChecking=no -p %PORT% %USER%@%SERVER% "mkdir -p /var/www/quiz-system && cd /var/www/quiz-system && rm -rf * && git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git ."
)

echo.
echo 第2步：安装后端依赖...
plink -batch -P %PORT% %USER%@%SERVER% "cd /var/www/quiz-system/backend && pip3 install -r requirements.txt 2>/dev/null || pip3 install flask flask-cors pymysql sqlalchemy python-dotenv xlsxwriter Werkzeug Jinja2"

echo.
echo 第3步：安装前端依赖并构建...
plink -batch -P %PORT% %USER%@%SERVER% "cd /var/www/quiz-system/frontend && npm install && npm run build"

echo.
echo 第4步：重启服务...
plink -batch -P %PORT% %USER%@%SERVER% "cd /var/www/quiz-system && pm2 restart all 2>/dev/null || (pm2 delete all 2>/dev/null && pm2 start backend/app.py --name quiz-backend && pm2 save)"

echo.
echo ========================================
echo 部署完成！
echo ========================================
pause
