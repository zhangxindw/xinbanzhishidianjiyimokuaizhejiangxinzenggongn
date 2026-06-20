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

# 杀死占用端口的进程
print("Killing processes using port 5001...")
result = run_cmd("pkill -f 'python.*app.py' || true")
print(result.stdout if result.stdout else "")
result = run_cmd("lsof -i :5001 || true")
print(result.stdout if result.stdout else "")

# 检查app.py中的端口配置
print("\nChecking app.py port configuration...")
result = run_cmd("grep -n 'port' /var/www/quiz-system/backend/app.py | head -10")
print(result.stdout if result.stdout else "")

# 重新启动后端
print("\nRestarting backend...")
result = run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 & sleep 3 && ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "")

# 检查端口
print("\nChecking ports...")
result = run_cmd("netstat -tlnp | grep python || lsof -i -P | grep python")
print(result.stdout if result.stdout else "")

# 测试API
print("\nTesting API...")
result = run_cmd("curl -s http://localhost/api/chapters")
print(result.stdout[:500] if result.stdout else "API not working")
