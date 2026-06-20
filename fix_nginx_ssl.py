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

print("=== Checking nginx error log ===")
result = run_cmd("tail -20 /var/log/nginx/error.log")
print(result.stdout if result.stdout else "")

print("\n=== Checking current config ===")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout)

print("\n=== Checking if symlink exists ===")
result = run_cmd("ls -la /etc/nginx/sites-enabled/")
print(result.stdout)

print("\n=== Checking nginx listen ports ===")
result = run_cmd("nginx -T 2>/dev/null | grep -E 'listen|ssl_certificate' | head -20")
print(result.stdout if result.stdout else "")

print("\n=== Restarting nginx ===")
result = run_cmd("systemctl restart nginx")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\n=== Checking port 443 after restart ===")
result = run_cmd("ss -tlnp | grep :443 || netstat -tlnp | grep :443 || echo 'Still not listening'")
print(result.stdout)
