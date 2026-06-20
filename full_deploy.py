import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

# Step 1: 克隆或更新代码
print("Step 1: Pulling code from GitHub...")
cmd1 = 'cd /var/www && rm -rf quiz-system 2>/dev/null; git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuaizhejiangxinzenggongn.git quiz-system'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd1],
    capture_output=True,
    text=True,
    timeout=180
)
print(f"Output: {result.stdout[:2000]}")
if result.stderr:
    print(f"Error: {result.stderr[:500]}")

print("\n" + "="*50 + "\n")

# Step 2: Build frontend
print("Step 2: Building frontend...")
cmd2 = 'cd /var/www/quiz-system/frontend && npm install && npm run build'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd2],
    capture_output=True,
    text=True,
    timeout=300
)
print(f"Output: {result.stdout[-3000:]}")
if result.stderr:
    print(f"Error: {result.stderr[-1000:]}")

print("\n" + "="*50 + "\n")

# Step 3: Install backend dependencies
print("Step 3: Installing backend dependencies...")
cmd3 = 'cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd3],
    capture_output=True,
    text=True,
    timeout=180
)
print(f"Output: {result.stdout[-2000:]}")
if result.stderr:
    print(f"Error: {result.stderr[-500:]}")

print("\n" + "="*50 + "\n")

# Step 4: Check and upgrade nginx if needed
print("Step 4: Checking nginx version...")
cmd4 = 'nginx -v 2>&1'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd4],
    capture_output=True,
    text=True,
    timeout=60
)
nginx_version = result.stdout + result.stderr
print(f"Nginx version: {nginx_version}")

# Check if version < 1.18
if '1.1' in nginx_version or '1.0' in nginx_version or '1.2' in nginx_version:
    print("Nginx version is old, upgrading...")
    cmd_upgrade = 'apt-get update && apt-get install -y nginx'
    result = subprocess.run(
        ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd_upgrade],
        capture_output=True,
        text=True,
        timeout=180
    )
    print(f"Upgrade output: {result.stdout[-1000:]}")
else:
    print("Nginx version is OK (1.18+)")

print("\n" + "="*50 + "\n")

# Step 5: Configure nginx
print("Step 5: Configuring nginx...")
nginx_config = '''server {
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

# Write nginx config
cmd_write_config = f'echo \'{nginx_config}\' > /etc/nginx/sites-available/quiz-system && ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system && rm -f /etc/nginx/sites-enabled/default'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd_write_config],
    capture_output=True,
    text=True,
    timeout=60
)
print(f"Config write: {result.stdout}")

# Test and reload nginx
cmd_reload = 'nginx -t && systemctl reload nginx'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd_reload],
    capture_output=True,
    text=True,
    timeout=60
)
print(f"Nginx test/reload: {result.stdout}")
if result.stderr:
    print(f"Error: {result.stderr}")

print("\n" + "="*50 + "\n")

# Step 6: Start backend
print("Step 6: Starting backend...")
cmd_start = 'cd /var/www/quiz-system/backend && pkill -f "python.*app.py" 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 &'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd_start],
    capture_output=True,
    text=True,
    timeout=60
)
print(f"Start output: {result.stdout}")

# Check status
cmd_status = 'sleep 3 && ps aux | grep app.py | grep -v grep && echo "Backend is running!"'
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd_status],
    capture_output=True,
    text=True,
    timeout=30
)
print(f"Status: {result.stdout}")
if result.stderr:
    print(f"Error: {result.stderr}")

print("\n" + "="*50)
print("Deployment completed!")
