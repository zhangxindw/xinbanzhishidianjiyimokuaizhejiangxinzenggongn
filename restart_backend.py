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

# 检查后端状态
print("Checking backend status...")
result = run_cmd("ps aux | grep app.py")
print(result.stdout if result.stdout else "No app.py process")

# 检查端口占用
print("\nChecking port 5001...")
result = run_cmd("netstat -tlnp 2>/dev/null | grep 5001 || ss -tlnp | grep 5001")
print(result.stdout if result.stdout else "Port 5001 not in use")

# 如果后端没运行，强制杀死并重启
print("\nForce killing and restarting backend...")
run_cmd("pkill -9 -f 'python.*app.py' || true")
result = run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 &")
print("Started backend")

result = run_cmd("sleep 5 && ps aux")
print(result.stdout[-500:] if result.stdout else "")
