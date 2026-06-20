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

print("=== Checking current nginx config ===")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout if result.stdout else "No config found")

print("\n=== Checking SSL certificate dir ===")
result = run_cmd("ls -la /etc/nginx/ssl/ 2>/dev/null || echo 'No SSL dir'")
print(result.stdout)

print("\n=== Checking nginx status ===")
result = run_cmd("systemctl status nginx --no-pager 2>&1 | head -20")
print(result.stdout)

print("\n=== Checking if port 443 is open ===")
result = run_cmd("netstat -tlnp | grep :443 || ss -tlnp | grep :443 || echo 'Port 443 not listening'")
print(result.stdout)
