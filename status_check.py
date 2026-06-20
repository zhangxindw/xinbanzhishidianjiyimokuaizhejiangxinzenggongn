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

print("=== Deployment Status ===\n")

# 1. 检查nginx
print("1. Nginx status:")
result = run_cmd("systemctl status nginx | head -5")
print(result.stdout if result.stdout else "Nginx running")

# 2. 检查后端
print("\n2. Backend status:")
result = run_cmd("ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend not running")

# 3. 测试网站
print("\n3. Website test:")
result = run_cmd("curl -s http://localhost/ | head -10")
print(result.stdout if result.stdout else "No response")

# 4. 测试API
print("\n4. API test (chapters):")
result = run_cmd("curl -s http://localhost/api/chapters | head -5")
print(result.stdout if result.stdout else "API not working")

# 5. 检查前端构建
print("\n5. Frontend build check:")
result = run_cmd("ls /var/www/quiz-system/frontend/dist/assets/ | wc -l")
print(f"Assets files: {result.stdout.strip()}")

# 6. 检查后端日志
print("\n6. Backend logs:")
result = run_cmd("tail -5 /tmp/app.log")
print(result.stdout if result.stdout else "No logs")

print("\n=== Deployment Complete ===")
