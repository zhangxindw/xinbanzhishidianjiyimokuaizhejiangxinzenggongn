import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=120):
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

print("=== Step 1: Stop backend ===")
run_cmd("pkill -f 'python.*app.py' || true")

print("=== Step 2: Backup server DB ===")
run_cmd("cp /var/www/quiz-system/backend/instance/quiz_system.db /var/www/quiz-system/backend/instance/quiz_system.db.bak.$(date +%s) 2>/dev/null || true")

print("=== Step 3: Upload local DB ===")
# Use PSCP to upload the database file
cmd = f'"D:\\putty\\pscp.exe" -scp -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" "d:\\桌面\\abc\\backend\\instance\\quiz_system.db" {user}@{server}:/var/www/quiz-system/backend/instance/quiz_system.db'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\n=== Step 4: Verify uploaded DB ===")
result = run_cmd("ls -la /var/www/quiz-system/backend/instance/quiz_system.db")
print(result.stdout)

print("\n=== Step 5: Restart backend ===")
run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 &")

print("\n=== Step 6: Verify API data ===")
import time
time.sleep(3)
result = run_cmd("curl -s http://localhost:5001/api/chapters")
print(result.stdout[:500] if result.stdout else "")

result = run_cmd("curl -s 'http://localhost:5001/api/questions?page=1&per_page=5'")
print(result.stdout[:500] if result.stdout else "")

print("\n=== Done ===")
