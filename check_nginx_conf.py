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

print("=== Full config file ===")
result = run_cmd("cat -n /etc/nginx/sites-available/quiz-system")
print(result.stdout if result.stdout else "")

print("\n=== Config file with special chars visible ===")
result = run_cmd("cat -A /etc/nginx/sites-available/quiz-system")
print(result.stdout if result.stdout else "")
