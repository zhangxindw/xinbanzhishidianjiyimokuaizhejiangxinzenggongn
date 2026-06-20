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

# 检查nginx配置内容
print("Checking nginx config...")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout)

# 直接写入配置文件
print("\nWriting config with printf...")
config_content = 'server { listen 80; server_name localhost; location / { root /var/www/quiz-system/frontend/dist; index index.html; try_files $uri $uri/ /index.html; } location /api { proxy_pass http://127.0.0.1:5000; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; } location /uploads { alias /var/www/quiz-system/backend/uploads; } }'
cmd = f"printf '%s' '{config_content}' > /etc/nginx/sites-available/quiz-system"
result = run_cmd(cmd)
print(result.stdout if result.stdout else "Written")

# 重新测试nginx
print("\nTesting nginx...")
result = run_cmd("nginx -t && systemctl reload nginx")
print(result.stdout)
print(result.stderr if result.stderr else "")

# 测试网站
print("\nTesting website (curl)...")
result = run_cmd("curl -s http://localhost/")
print(result.stdout[:500] if result.stdout else "No response")

# 检查前端dist目录
print("\nChecking dist directory...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/")
print(result.stdout)
