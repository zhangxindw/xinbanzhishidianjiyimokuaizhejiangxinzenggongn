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

# 检查nginx配置
print("Current nginx config:")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout if result.stdout else "")

# 检查后端状态
print("\nBackend status:")
result = run_cmd("ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "")

# 检查端口
print("\nPort status:")
result = run_cmd("netstat -tlnp | grep 5001")
print(result.stdout if result.stdout else "")

# 检查nginx错误日志
print("\nNginx error log:")
result = run_cmd("tail -10 /var/log/nginx/error.log")
print(result.stdout if result.stdout else "")

# 重新启动nginx
print("\nRestarting nginx...")
result = run_cmd("systemctl restart nginx")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

# 再次测试
print("\nTesting again:")
result = run_cmd("curl -s http://localhost/api/chapters")
print(result.stdout if result.stdout else "")
