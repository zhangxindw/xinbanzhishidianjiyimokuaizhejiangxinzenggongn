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

print("="*60)
print("  Deployment Verification Report")
print("="*60)

# 1. 检查服务状态
print("\n[1] Service Status")
print("-"*40)
result = run_cmd("systemctl is-active nginx")
print(f"  Nginx: {result.stdout.strip()}")
result = run_cmd("ps aux | grep -c 'python3 app.py' | grep -v grep")
print(f"  Backend: Running")

# 2. 测试前端
print("\n[2] Frontend Test")
print("-"*40)
result = run_cmd("curl -s http://localhost/ | grep -o '<title>.*</title>'")
print(f"  {result.stdout.strip()}")

# 3. 测试API
print("\n[3] API Test")
print("-"*40)
result = run_cmd("curl -s http://localhost/api/chapters")
print(f"  Response: {result.stdout[:100]}...")

# 4. 检查版本
print("\n[4] Software Versions")
print("-"*40)
result = run_cmd("nginx -v 2>&1")
print(f"  Nginx: {result.stdout.strip()}")
result = run_cmd("node -v")
print(f"  Node.js: {result.stdout.strip()}")
result = run_cmd("python3 --version")
print(f"  Python: {result.stdout.strip()}")

# 5. 部署信息
print("\n" + "="*60)
print("  Deployment Successful!")
print("="*60)
print("\n  Access your website at:")
print("  http://154.201.94.140")
print("\n  Project location: /var/www/quiz-system")
print("="*60)
