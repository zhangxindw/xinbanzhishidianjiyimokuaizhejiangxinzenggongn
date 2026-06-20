import subprocess
import os

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

# 使用 -pw 直接传递密码
cmd = 'echo "test connection" && pwd && ls /var/www/'

# 创建临时命令文件
cmd_file = os.path.join(os.environ['TEMP'], 'plink_commands.txt')
with open(cmd_file, 'w') as f:
    f.write(cmd)

# 直接使用 shell=True 并传递密码
result = subprocess.run(
    f'"D:\\putty\\plink.exe" -ssh -batch -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" {user}@{server} "{cmd}"',
    shell=True,
    capture_output=True,
    text=True,
    timeout=60
)

print(f"STDOUT:\n{result.stdout}")
print(f"STDERR:\n{result.stderr}")
print(f"Return code: {result.returncode}")
