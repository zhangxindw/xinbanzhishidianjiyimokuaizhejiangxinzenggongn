import subprocess
import os

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=300):
    print(f"\n{'='*60}")
    print(f"Executing: {cmd[:100]}...")
    print(f"{'='*60}")
    
    result = subprocess.run(
        f'"D:\\putty\\plink.exe" -ssh -batch -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" {user}@{server} "{cmd}"',
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    
    print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Error:\n{result.stderr}")
    print(f"Return code: {result.returncode}")
    return result.returncode == 0

# Step 1: 创建目录并克隆仓库
print("\n" + "="*60)
print("Step 1: Creating directory and cloning repository")
print("="*60)
run_cmd("mkdir -p /var/www && cd /var/www && rm -rf quiz-system 2>/dev/null; git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuaizhejiangxinzenggongn.git quiz-system", timeout=300)

# Step 2: 检查仓库
print("\n" + "="*60)
print("Step 2: Verify repository")
print("="*60)
run_cmd("ls -la /var/www/quiz-system/")

# Step 3: 检查nginx版本
print("\n" + "="*60)
print("Step 3: Check nginx version")
print("="*60)
run_cmd("nginx -v 2>&1")

# Step 4: 安装npm依赖并构建前端
print("\n" + "="*60)
print("Step 4: Install npm and build frontend")
print("="*60)
run_cmd("which npm || (apt-get update && apt-get install -y npm)", timeout=120)
run_cmd("cd /var/www/quiz-system/frontend && npm install", timeout=300)
run_cmd("cd /var/www/quiz-system/frontend && npm run build", timeout=300)

# Step 5: 安装Python依赖
print("\n" + "="*60)
print("Step 5: Install Python dependencies")
print("="*60)
run_cmd("cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple", timeout=300)

# Step 6: 配置nginx
print("\n" + "="*60)
print("Step 6: Configure nginx")
print("="*60)

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

# 创建nginx配置
cmd_create_conf = f'mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled && echo "{nginx_conf}" > /etc/nginx/sites-available/quiz-system'
run_cmd(cmd_create_conf)
run_cmd("ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system && rm -f /etc/nginx/sites-enabled/default")

# 测试nginx配置
run_cmd("nginx -t")
run_cmd("systemctl reload nginx")

# Step 7: 启动后端
print("\n" + "="*60)
print("Step 7: Start backend")
print("="*60)
run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 &")
run_cmd("sleep 3 && ps aux | grep app.py | grep -v grep")

print("\n" + "="*60)
print("Deployment completed!")
print("="*60)
