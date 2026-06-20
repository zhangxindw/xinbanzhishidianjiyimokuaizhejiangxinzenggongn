import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=300, decode_errors='replace'):
    result = subprocess.run(
        f'"D:\\putty\\plink.exe" -ssh -batch -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" {user}@{server} "{cmd}"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding='utf-8',
        errors=decode_errors
    )
    return result

# Step 1: 重新克隆仓库
print("Step 1: Re-cloning repository...")
result = run_cmd("cd /var/www && rm -rf quiz-system && git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuaizhejiangxinzenggongn.git quiz-system", timeout=300)
print(result.stdout if result.stdout else "No output")

# Step 2: 检查文件
print("\nStep 2: Checking files...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/src/views/DistinguishManagementView.vue")
print(result.stdout)

# Step 3: 构建前端
print("\nStep 3: Building frontend...")
result = run_cmd("cd /var/www/quiz-system/frontend && npm install && npm run build", timeout=600)
print(result.stdout[-3000:] if result.stdout else "No output")

# Step 4: 检查构建结果
print("\nStep 4: Checking build output...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/")
print(result.stdout)

# Step 5: 配置nginx
print("\nStep 5: Configuring nginx...")
nginx_conf = '''server {
    listen 80;
    server_name localhost;

    location / {
        root /var/www/quiz-system/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads {
        alias /var/www/quiz-system/backend/uploads;
    }
}'''

result = run_cmd(f"mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled && echo \"{nginx_conf}\" > /etc/nginx/sites-available/quiz-system")
print(result.stdout if result.stdout else "Config written")

result = run_cmd("ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system && rm -f /etc/nginx/sites-enabled/default")
result = run_cmd("nginx -t && systemctl reload nginx")
print(result.stdout)

# Step 6: 启动后端
print("\nStep 6: Starting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple", timeout=300)
print(result.stdout[-1000:] if result.stdout else "Dependencies installed")

result = run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend check")

# Step 7: 测试网站
print("\nStep 7: Testing website...")
result = run_cmd("curl -s http://localhost/ | head -20")
print(result.stdout if result.stdout else "Website check")

print("\nDone!")
