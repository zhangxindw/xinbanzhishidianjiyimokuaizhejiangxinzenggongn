import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

cmd = 'find /var/www -type d -name ".git" 2>/dev/null | head -5'
print(f"Executing: {cmd}")
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd],
    capture_output=True,
    text=True,
    timeout=60
)
print(f"Output: {result.stdout}")
if result.stderr:
    print(f"Error: {result.stderr}")
print(f"Return code: {result.returncode}")