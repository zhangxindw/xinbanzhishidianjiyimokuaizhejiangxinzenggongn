import subprocess
import time

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

print("=== Pull from correct repo ===")
result = run_cmd("cd /var/www/quiz-system && git pull origin main")
print(result.stdout)
print(result.stderr if result.stderr else "")

print("\n=== Check database size ===")
result = run_cmd("ls -la /var/www/quiz-system/backend/instance/quiz_system.db")
print(result.stdout)

print("\n=== Stop backend ===")
run_cmd("pkill -f 'python.*app.py' || true")

print("\n=== Restart backend ===")
run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 &")
time.sleep(3)

print("\n=== Test API ===")
result = run_cmd("curl -s http://localhost:5001/api/chapters")
print("Chapters:", result.stdout[:500] if result.stdout else "")

result = run_cmd("curl -s 'http://localhost:5001/api/questions?page=1&per_page=5'")
print("Questions:", result.stdout[:500] if result.stdout else "")

print("\n=== Test HTTPS ===")
result = run_cmd("curl -sk https://www.zxruankaoshuati.fun/api/chapters")
print("HTTPS API:", result.stdout[:300] if result.stdout else "")