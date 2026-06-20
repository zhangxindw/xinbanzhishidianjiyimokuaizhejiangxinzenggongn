import subprocess
import base64
import time

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

print("=== Step 3: Encode local DB ===")
with open(r'd:\桌面\abc\backend\instance\quiz_system.db', 'rb') as f:
    db_data = f.read()
encoded = base64.b64encode(db_data).decode('ascii')
print(f"Database size: {len(db_data)} bytes, Base64 chunks: {(len(encoded) // 1000) + 1}")

print("=== Step 4: Upload to server in chunks ===")
# Clear target file
run_cmd("rm -f /tmp/db_base64.txt")

# Write in chunks of 900 chars to avoid command length limits
chunk_size = 900
for i in range(0, len(encoded), chunk_size):
    chunk = encoded[i:i+chunk_size]
    run_cmd(f"echo -n '{chunk}' >> /tmp/db_base64.txt")
    if (i // chunk_size) % 50 == 0:
        print(f"  Progress: {i}/{len(encoded)}")

print("=== Step 5: Decode on server ===")
run_cmd("base64 -d /tmp/db_base64.txt > /var/www/quiz-system/backend/instance/quiz_system.db")
run_cmd("rm -f /tmp/db_base64.txt")

print("=== Step 6: Verify ===")
result = run_cmd("ls -la /var/www/quiz-system/backend/instance/quiz_system.db")
print(result.stdout)

print("\n=== Step 7: Restart backend ===")
run_cmd("cd /var/www/quiz-system/backend && nohup python3 app.py > /tmp/app.log 2>&1 &")

time.sleep(3)

print("\n=== Step 8: Verify API data ===")
result = run_cmd("curl -s http://localhost:5001/api/chapters")
print("Chapters:", result.stdout[:300] if result.stdout else "")

result = run_cmd("curl -s 'http://localhost:5001/api/questions?page=1&per_page=3'")
print("Questions:", result.stdout[:300] if result.stdout else "")

print("\n=== Done ===")
