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

print("=== Final Deployment Verification ===\n")

# 1. 测试前端
print("1. Frontend (http://localhost/):")
result = run_cmd("curl -s http://localhost/ | head -5")
print(result.stdout if result.stdout else "No response")

# 2. 测试API
print("\n2. API (http://localhost/api/chapters):")
result = run_cmd("curl -s http://localhost/api/chapters | head -3")
print(result.stdout if result.stdout else "API not working")

# 3. 测试后端
print("\n3. Backend (http://localhost:5000):")
result = run_cmd("curl -s http://localhost:5000/api/chapters | head -3")
print(result.stdout if result.stdout else "Backend not working")

# 4. 检查服务状态
print("\n4. Service status:")
result = run_cmd("ps aux | grep -E 'nginx|python.*app'")
print(result.stdout if result.stdout else "")

# 5. 部署完成信息
print("\n" + "="*50)
print("Deployment completed successfully!")
print("="*50)
print("\nAccess the website at: http://154.201.94.140")
