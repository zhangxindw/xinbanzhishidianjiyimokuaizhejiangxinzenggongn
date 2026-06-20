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

# Step 1: 检查并安装Python pip
print("Step 1: Installing pip...")
result = run_cmd("which pip3 || apt-get install -y python3-pip")
print(result.stdout[-500:] if result.stdout else "No output")

# Step 2: 安装Python依赖
print("\nStep 2: Installing Python dependencies...")
result = run_cmd("cd /var/www/quiz-system/backend && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")
if result.stderr:
    print(f"Error: {result.stderr[-500:]}")

# Step 3: 检查Node版本
print("\nStep 3: Checking Node version...")
result = run_cmd("node -v && npm -v")
print(result.stdout)

# Step 4: 清理并重新构建前端
print("\nStep 4: Rebuilding frontend...")
result = run_cmd("cd /var/www/quiz-system/frontend && rm -rf node_modules/.vite && npm run build 2>&1", timeout=300)
print(result.stdout[-3000:] if result.stdout else "No output")
if result.stderr:
    print(f"Stderr: {result.stderr[-1000:]}")

# Step 5: 检查构建结果
print("\nStep 5: Checking build output...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/")
print(result.stdout)

# Step 6: 重启后端
print("\nStep 6: Restarting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend check")
if result.stderr:
    print(f"Error: {result.stderr}")

print("\nDone!")
