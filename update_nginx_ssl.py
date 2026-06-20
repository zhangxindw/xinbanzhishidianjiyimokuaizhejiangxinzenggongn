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

# Write nginx config using cat with heredoc
print("Writing nginx config...")
config = '''server {
    listen 80;
    server_name www.zxruankaoshuati.fun zxruankaoshuati.fun;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name www.zxruankaoshuati.fun zxruankaoshuati.fun;

    ssl_certificate /etc/nginx/ssl/www.zxruankaoshuati.fun.pem;
    ssl_certificate_key /etc/nginx/ssl/www.zxruankaoshuati.fun.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        root /var/www/quiz-system/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /var/www/quiz-system/backend/uploads;
    }
}'''

# Use echo to write file line by line (avoid quoting issues)
run_cmd("rm -f /etc/nginx/sites-available/quiz-system")
for line in config.split('\n'):
    safe_line = line.replace("'", "'\\''").replace('"', '\\"')
    run_cmd(f"echo '{safe_line}' >> /etc/nginx/sites-available/quiz-system")

print("\nVerifying config...")
result = run_cmd("cat /etc/nginx/sites-available/quiz-system")
print(result.stdout)

print("\nTesting nginx config...")
result = run_cmd("nginx -t")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\nRestarting nginx...")
result = run_cmd("systemctl restart nginx")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\nChecking port 443...")
result = run_cmd("ss -tlnp | grep :443 || netstat -tlnp | grep :443 || echo 'Not listening'")
print(result.stdout)
