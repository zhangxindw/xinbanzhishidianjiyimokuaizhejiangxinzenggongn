# 部署到服务器
$server = "154.201.94.140"
$port = 22
$user = "root"
$pass = "6dwic8N532a7"

$remoteCommands = @"
cd /var/www/quiz-system
git pull origin main
cd frontend
npm run build
cd ..
pkill -f 'python.*app.py' || true
nohup python3 app.py > /tmp/app.log 2>&1 &
sleep 3
ps aux | grep app.py | grep -v grep
echo 'Deploy completed!'
"@

$expectScript = @"
#!/usr/bin/expect -f
set timeout 120
spawn ssh -o StrictHostKeyChecking=no -p $port $user@$server
expect {
    ""password:"" {
        send ""$pass\r""
    }
    timeout {
        exit 1
    }
}
expect ""~#""
send ""$remoteCommands\r""
send ""exit\r""
expect eof
"@

$expectScript | Out-File -FilePath "$env:TEMP\deploy.exp" -Encoding utf8
& expect "$env:TEMP\deploy.exp"
