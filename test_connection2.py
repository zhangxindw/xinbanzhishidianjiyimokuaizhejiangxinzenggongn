import subprocess
import os

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

# 使用 plink -m 从文件读取命令
cmd = 'echo "test connection" && pwd && nginx -v 2>&1'

# 创建临时命令文件
cmd_file = os.path.join(os.environ['TEMP'], 'plink_commands.txt')
with open(cmd_file, 'w') as f:
    f.write(cmd)

proc = subprocess.Popen(
    ['D:\\putty\\plink.exe', '-ssh', '-batch', '-m', cmd_file,
     f'{user}@{server}', '-P', str(port), '-hostkey', 'ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

stdout, _ = proc.communicate(timeout=60)
print(f"Output:\n{stdout}")
print(f"Return code: {proc.returncode}")
