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

# 修复nginx配置 - 后端运行在5001端口
print("Fixing nginx configuration...")
nginx_conf = '''server {
    listen 80;
    server_name localhost;

    location / {
        root /var/www/quiz-system/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads {
        alias /var/www/quiz-system/backend/uploads;
    }
}'''

# 写入配置文件
cmd = f"printf '%s' '{nginx_conf}' > /etc/nginx/sites-available/quiz-system"
result = run_cmd(cmd)
print("Config written")

# 重新加载nginx
print("\nReloading nginx...")
result = run_cmd("nginx -t && systemctl reload nginx")
print(result.stdout)
print(result.stderr if result.stderr else "")

# 测试API
print("\nTesting API through nginx...")
result = run_cmd("curl -s http://localhost/api/chapters | head -3")
print(result.stdout if result.stdout else "")
