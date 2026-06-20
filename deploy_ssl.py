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

# Step 1: Create SSL directory
print("Creating SSL directory...")
run_cmd("mkdir -p /etc/nginx/ssl")

# Step 2: Upload certificate files using PSCP
print("Uploading SSL certificates...")

# Use pscp to upload files
cmd_key = f'"D:\\putty\\pscp.exe" -scp -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" "d:\\桌面\\abc\\www.zxruankaoshuati.fun.key" {user}@{server}:/etc/nginx/ssl/'
result = subprocess.run(cmd_key, shell=True, capture_output=True, text=True, timeout=60)
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

cmd_pem = f'"D:\\putty\\pscp.exe" -scp -pw {password} -P {port} -hostkey "ssh-ed25519 255 c4:eb:cb:b9:7d:fa:d6:9b:f7:29:3c:33:c3:54:1f:16" "d:\\桌面\\abc\\www.zxruankaoshuati.fun.pem" {user}@{server}:/etc/nginx/ssl/'
result = subprocess.run(cmd_pem, shell=True, capture_output=True, text=True, timeout=60)
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

# Step 3: Verify files uploaded
print("\nVerifying uploaded files...")
result = run_cmd("ls -la /etc/nginx/ssl/")
print(result.stdout)

# Step 4: Update nginx config with SSL
print("\nUpdating nginx config...")
nginx_conf = '''server {
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

cmd = f"printf '%s' '{nginx_conf}' > /etc/nginx/sites-available/quiz-system"
result = run_cmd(cmd)
print("Config written")

# Step 5: Test and reload nginx
print("\nTesting nginx config...")
result = run_cmd("nginx -t")
print(result.stdout if result.stdout else "")
print(result.stderr if result.stderr else "")

print("\nReloading nginx...")
result = run_cmd("systemctl reload nginx")
print("Nginx reloaded" if result.returncode == 0 else f"Failed: {result.stderr}")

# Step 6: Check port 443
print("\nChecking port 443...")
result = run_cmd("ss -tlnp | grep :443 || netstat -tlnp | grep :443")
print(result.stdout if result.stdout else "Port 443 not listening")
