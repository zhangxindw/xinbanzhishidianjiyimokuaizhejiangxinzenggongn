import subprocess
import sys

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=60):
    print(f"\n{'='*50}")
    print(f"Executing: {cmd[:80]}...")
    print(f"{'='*50}")
    
    # 使用plink，需要通过stdin传递密码
    proc = subprocess.Popen(
        ['D:\\putty\\plink.exe', '-ssh', '-batch', 
         f'{user}@{server}', '-P', str(port), '-hostkey', 'ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16',
         cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        print(f"Output:\n{stdout}")
        if stderr:
            print(f"Error:\n{stderr}")
        return proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        print(f"Command timed out after {timeout} seconds")
        return -1

# Step 1: 检查目录
print("\n=== Step 1: Checking project directory ===")
run_cmd("ls -la /var/www/quiz-system 2>/dev/null || echo 'Directory does not exist'", timeout=30)

# Step 2: 如果目录不存在，克隆仓库
print("\n=== Step 2: Clone repository ===")
run_cmd("cd /var/www && rm -rf quiz-system 2>/dev/null; git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuaizhejiangxinzenggongn.git quiz-system", timeout=180)

# Step 3: 构建前端
print("\n=== Step 3: Build frontend ===")
run_cmd("cd /var/www/quiz-system/frontend && npm install && npm run build", timeout=300)

# Step 4: 安装后端依赖
print("\n=== Step 4: Install backend dependencies ===")
run_cmd("cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple", timeout=180)

# Step 5: 配置nginx
print("\n=== Step 5: Configure nginx ===")
nginx_conf = '''server {{
    listen 80;
    server_name localhost;

    location / {{
        root /var/www/quiz-system/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }}

    location /api {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}

    location /uploads {{
        alias /var/www/quiz-system/backend/uploads;
    }}
}}'''

# 写入nginx配置
run_cmd(f"echo '{nginx_conf}' > /etc/nginx/sites-available/quiz-system", timeout=30)
run_cmd("ln -sf /etc/nginx/sites-available/quiz-system /etc/nginx/sites-enabled/quiz-system && rm -f /etc/nginx/sites-enabled/default", timeout=30)

# 检查nginx版本并重新加载
print("\n=== Step 6: Check nginx and reload ===")
run_cmd("nginx -v 2>&1", timeout=30)
run_cmd("nginx -t && systemctl reload nginx", timeout=30)

# Step 7: 启动后端
print("\n=== Step 7: Start backend ===")
run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 &", timeout=30)
run_cmd("sleep 3 && ps aux | grep app.py | grep -v grep", timeout=30)

print("\n" + "="*50)
print("Deployment completed!")
print("="*50)
