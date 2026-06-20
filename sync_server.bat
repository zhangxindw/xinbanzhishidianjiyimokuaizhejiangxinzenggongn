@echo off
chcp 65001 >nul
echo 正在连接服务器并拉取代码...
echo.
echo 6dwic8N532a7 | ssh -o StrictHostKeyChecking=no -o BatchMode=yes root@154.201.94.140 "cd /root/xinbanzhishidianjiyimokuaizhejiang 2>/dev/null && git pull new_origin main 2>&1 || echo 项目目录不存在，正在克隆..."
echo.
echo 按任意键退出...
pause >nul
