import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

cmd = 'nginx -v 2>&1; cat /etc/os-release | grep PRETTY_NAME'
print(f"Executing: {cmd}")
result = subprocess.run(
    ['D:\\putty\\plink.exe', '-ssh', f'{user}@{server}', '-pw', password, '-P', str(port), cmd],
    capture_output=True,
    text=True,
    timeout=120
)
print(f"Output: {result.stdout}")
if result.stderr:
    print(f"Error: {result.stderr}")
print(f"Return code: {result.returncode}")
