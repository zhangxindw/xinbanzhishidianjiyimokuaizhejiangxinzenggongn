import subprocess

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

cmd = 'echo "test connection" && pwd && nginx -v 2>&1 && node -v 2>&1 && python3 --version'

proc = subprocess.Popen(
    ['D:\\putty\\plink.exe', '-ssh', '-batch', 
     f'{user}@{server}', '-P', str(port), '-hostkey', 'ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16',
     cmd],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = proc.communicate(timeout=60)
print(f"STDOUT:\n{stdout}")
print(f"STDERR:\n{stderr}")
print(f"Return code: {proc.returncode}")
