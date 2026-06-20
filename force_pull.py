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

print("=== Check git remote ===")
result = run_cmd("cd /var/www/quiz-system && git remote -v")
print(result.stdout)

print("\n=== Check git log ===")
result = run_cmd("cd /var/www/quiz-system && git log --oneline -3")
print(result.stdout)

print("\n=== Force pull from correct repo ===")
# The server might be using a different repo, let me fetch from the correct one
result = run_cmd("cd /var/www/quiz-system && git fetch https://github.com/zhangxindw/ruankaoshuatixitong.git main && git reset --hard FETCH_HEAD")
print(result.stdout)
print(result.stderr if result.stderr else "")

print("\n=== Check database size now ===")
result = run_cmd("ls -la /var/www/quiz-system/backend/instance/")
print(result.stdout)