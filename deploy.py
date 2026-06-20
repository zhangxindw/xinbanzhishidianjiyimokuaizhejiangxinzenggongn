import subprocess
import time

server = "154.201.94.140"
port = 22
user = "root"
password = "6dwic8N532a7"

commands = [
    f'cd /var/www/quiz-system && git pull origin main',
    f'cd /var/www/quiz-system/frontend && npm run build',
    f'cd /var/www/quiz-system && pkill -f "python.*app.py" || true && nohup python3 app.py > /tmp/app.log 2>&1 &',
    f'sleep 3 && ps aux | grep app.py | grep -v grep && echo "Deploy completed!"'
]

for cmd in commands:
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
    print("-" * 50)
