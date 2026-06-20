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
        timeout=timeout,
        encoding='utf-8',
        errors='replace'
    )
    return result

# 修复vite权限并构建
print("Fixing vite permission and building...")
result = run_cmd("cd /var/www/quiz-system/frontend && chmod +x node_modules/.bin/vite && node node_modules/vite/bin/vite.js build 2>&1", timeout=300)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return:", result.returncode)

# 检查构建结果
print("\nChecking build output...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/")
print(result.stdout)

if 'assets' in result.stdout and result.returncode == 0:
    print("\nConfiguring nginx...")
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
    
    cmd_conf = f"mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled && echo \"{nginx_conf}\" > /etc/nginx/sites-available/quiz-system"
    result = run_cmd(cmd_conf)
    
    result = run_cmd("ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system && rm -f /etc/nginx/sites-enabled/default && nginx -t && systemctl reload nginx")
    print(result.stdout)
    
    # 启动后端
    print("\nStarting backend...")
    result = run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
    print(result.stdout)
    
    # 测试网站
    print("\nTesting website...")
    result = run_cmd("curl -s http://localhost/ | head -30")
    print(result.stdout)
    
    print("\nDeployment completed!")
