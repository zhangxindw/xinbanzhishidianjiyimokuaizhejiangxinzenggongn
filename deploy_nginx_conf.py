import subprocess
import base64

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

# Read local config file
with open('d:\\桌面\\abc\\nginx_quiz.conf', 'r', encoding='utf-8') as f:
    config_content = f.read()

# Encode to base64
encoded = base64.b64encode(config_content.encode('utf-8')).decode('ascii')

print("Uploading config via base64...")
# Write base64 to file and decode on server
run_cmd(f"echo '{encoded}' | base64 -d > /etc/nginx/sites-available/quiz-system")

print("\nVerifying config...")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout[:500] if result.stdout else "")

print("\nTesting nginx...")
result = run_cmd("nginx -t")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\nRestarting nginx...")
result = run_cmd("systemctl restart nginx")

print("\nChecking ports...")
result = run_cmd("ss -tlnp | grep -E ':80|:443'")
print(result.stdout if result.stdout else "No ports listening")
