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

# Step 1: 升级Node.js到v18
print("Step 1: Upgrading Node.js to v18...")
result = run_cmd("curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")

# Step 2: 验证Node版本
print("\nStep 2: Verify Node.js version...")
result = run_cmd("node -v && npm -v")
print(result.stdout)

# Step 3: 清理并重新安装依赖
print("\nStep 3: Clean and reinstall npm dependencies...")
result = run_cmd("cd /var/www/quiz-system/frontend && rm -rf node_modules && npm install", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")
if result.stderr:
    print(f"Error: {result.stderr[-500:]}")

# Step 4: 构建前端
print("\nStep 4: Building frontend...")
result = run_cmd("cd /var/www/quiz-system/frontend && npm run build", timeout=300)
print(result.stdout[-2000:] if result.stdout else "No output")
if result.stderr:
    print(f"Stderr: {result.stderr[-500:]}")

# Step 5: 检查构建结果
print("\nStep 5: Checking build output...")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/")
print(result.stdout)

# Step 6: 重启后端
print("\nStep 6: Restarting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && pkill -f 'python.*app.py' 2>/dev/null; nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend check")

# Step 7: 测试网站
print("\nStep 7: Testing website...")
result = run_cmd("curl -s http://localhost/ | head -20")
print(result.stdout if result.stdout else "Website check")

print("\nDone!")
