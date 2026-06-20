import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=300):
    result = subprocess.run(
        f'"D:\\putty\\plink.exe" -ssh -batch -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" {user}@{server} "{cmd}"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    return result

# Step 1: 安装nginx和npm
print("Step 1: Installing nginx and npm...")
result = run_cmd("apt-get update && apt-get install -y nginx npm curl")
print(result.stdout[-2000:] if result.stdout else "No output")
print(f"Return: {result.returncode}")

# Step 2: 检查nginx版本
print("\nStep 2: Checking nginx version...")
result = run_cmd("nginx -v 2>&1")
print(result.stdout)

# Step 3: 安装npm依赖
print("\nStep 3: Installing npm dependencies...")
result = run_cmd("cd /var/www/quiz-system/frontend && npm install", timeout=600)
print(result.stdout[-2000:] if result.stdout else "No output")
print(f"Return: {result.returncode}")

# Step 4: 构建前端
print("\nStep 4: Building frontend...")
result = run_cmd("cd /var/www/quiz-system/frontend && npm run build", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")
print(f"Return: {result.returncode}")

# Step 5: 安装Python依赖
print("\nStep 5: Installing Python dependencies...")
result = run_cmd("cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")
print(f"Return: {result.returncode}")

# Step 6: 配置nginx
print("\nStep 6: Configuring nginx...")
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
print(result.stdout if result.stdout else "Symlink created")

# 测试nginx
result = run_cmd("nginx -t")
print(result.stdout)
result = run_cmd("systemctl reload nginx || nginx")
print(result.stdout if result.stdout else "Nginx reloaded")

# Step 7: 启动后端
print("\nStep 7: Starting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 &")
print(result.stdout if result.stdout else "Backend started")

result = run_cmd("sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend check")

print("\nDeployment completed!")
