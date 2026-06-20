import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=60):
    result = subprocess.run(
        f'"D:\\putty\\plink.exe" -ssh -batch -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" {user}@{server} "{cmd}"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        encoding='utf-8',
        errors='replace'
    )
    return result

# 创建nginx配置
print("Creating nginx configuration...")
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

# 使用cat heredoc创建配置文件
cmd = f'cat > /etc/nginx/sites-available/quiz-system << "EOF"\n{nginx_conf}\nEOF'
result = run_cmd(cmd)
print(result.stdout if result.stdout else "Config created")
print(result.stderr if result.stderr else "")

# 检查配置
print("\nChecking config file...")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout)

# 创建符号链接
print("\nCreating symlink...")
result = run_cmd("ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system")
print(result.stdout if result.stdout else "")

# 测试nginx配置
print("\nTesting nginx config...")
result = run_cmd("nginx -t")
print(result.stdout)
print(result.stderr)

# 重新加载nginx
print("\nReloading nginx...")
result = run_cmd("systemctl reload nginx")
print(result.stdout if result.stdout else "nginx reloaded")
print(result.stderr if result.stderr else "")

# 测试网站
print("\nTesting website...")
result = run_cmd("curl -s http://localhost/ | head -30")
print(result.stdout)

# 启动后端
print("\nStarting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend started")

# 测试API
print("\nTesting API...")
result = run_cmd("curl -s http://localhost/api/chapters | head -10")
print(result.stdout if result.stdout else "API test")
