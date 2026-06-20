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

print("=== Check backend process ===")
result = run_cmd("ps aux | grep app.py | grep -v grep")
print(result.stdout if result.stdout else "No backend running")

print("\n=== Check port 5001 ===")
result = run_cmd("ss -tlnp | grep 5001 || netstat -tlnp | grep 5001 || echo 'Port 5001 not listening'")
print(result.stdout)

print("\n=== Test API directly ===")
result = run_cmd("curl -s http://localhost:5001/api/chapters 2>&1")
print(result.stdout[:500] if result.stdout else "")

print("\n=== Test HTTPS ===")
result = run_cmd("curl -sk https://www.zxruankaoshuati.fun/api/chapters 2>&1")
print(result.stdout[:500] if result.stdout else "")