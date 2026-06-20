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

# 检查后端运行状态
print("Checking backend...")
result = run_cmd("ps aux | grep python3")
print(result.stdout if result.stdout else "")

# 检查端口
print("\nChecking ports...")
result = run_cmd("netstat -tlnp 2>/dev/null || ss -tlnp")
print(result.stdout if result.stdout else "")

# 检查后端日志
print("\nBackend logs:")
result = run_cmd("cat /tmp/app.log | tail -10")
print(result.stdout if result.stdout else "")

# 直接测试后端
print("\nDirect backend test:")
result = run_cmd("curl -s http://127.0.0.1:5001/api/chapters | head -3")
print(result.stdout if result.stdout else "")
