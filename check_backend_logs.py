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

print("=== Backend Logs ===")
result = run_cmd("cat /tmp/app.log | tail -50")
print(result.stdout if result.stdout else "No logs")

print("\n=== Checking Database File ===")
result = run_cmd("ls -la /var/www/quiz-system/backend/*.db 2>/dev/null || echo 'No db files found'")
print(result.stdout)

print("\n=== Checking Backend Process ===")
result = run_cmd("ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "Backend not running")

print("\n=== Testing API Directly ===")
result = run_cmd("curl -s http://localhost:5001/api/init-db 2>&1")
print(result.stdout[:1000] if result.stdout else "")
