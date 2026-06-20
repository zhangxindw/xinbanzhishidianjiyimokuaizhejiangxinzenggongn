import subprocess
import time

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

def run_cmd(cmd, timeout=300):
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

print("=== Step 1: Pull latest code ===")
result = run_cmd("cd /var/www/quiz-system && git pull origin main")
print(result.stdout)

print("\n=== Step 2: Rebuild frontend ===")
result = run_cmd("cd /var/www/quiz-system/frontend && npm run build 2>&1", timeout=300)
print(result.stdout[-500:] if result.stdout else "")
print(result.stderr[-200:] if result.stderr else "")

print("\n=== Step 3: Verify build ===")
result = run_cmd("ls -la /var/www/quiz-system/frontend/dist/ | head -5")
print(result.stdout)

print("\n=== Done ===")