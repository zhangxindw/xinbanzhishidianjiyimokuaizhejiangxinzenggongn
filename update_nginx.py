import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=30):
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

# 使用echo和tee来创建配置文件
print("Creating nginx config...")
config = 'server { listen 80; server_name localhost; location / { root /var/www/quiz-system/frontend/dist; index index.html; try_files $uri $uri/ /index.html; } location /api { proxy_pass http://127.0.0.1:5001; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; } location /uploads { alias /var/www/quiz-system/backend/uploads; } }'

# 使用echo命令写入
cmd = f"echo '{config}' | tee /etc/nginx/sites-available/quiz-system > /dev/null"
result = run_cmd(cmd)
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

# 验证写入
print("\nVerifying config:")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout)

# 重新加载nginx
print("\nReloading nginx...")
result = run_cmd("nginx -t && systemctl reload nginx")
print(result.stdout)
print(result.stderr if result.stderr else "")

# 测试
print("\nTesting API:")
result = run_cmd("curl -s http://localhost/api/chapters")
print(result.stdout[:500] if result.stdout else "")
