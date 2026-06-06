# 部署脚本
$server = "45.192.97.233"
$port = 22
$user = "root"
$pass = "K4NHWFAPDGsX"

# 创建远程命令脚本
$remoteCommands = @"
mkdir -p /var/www/quiz-system
cd /var/www/quiz-system
rm -rf *
git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
exit
"@

# 使用SSH执行命令
$cmd = "sshpass -p '$pass' ssh -o StrictHostKeyChecking=no -p $port $user@$server '$remoteCommands'"

# 由于sshpass不可用，尝试使用expect
$expectScript = @"
#!/usr/bin/expect -f
set timeout 120
spawn ssh -o StrictHostKeyChecking=no -p $port $user@$server
expect {
    "password:" {
        send "$pass\r"
    }
    timeout {
        exit 1
    }
}
expect "~#"
send "mkdir -p /var/www/quiz-system\r"
send "cd /var/www/quiz-system\r"
send "rm -rf *\r"
send "git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .\r"
send "exit\r"
expect eof
"@

# 保存expect脚本
$expectScript | Out-File -FilePath "$env:TEMP\deploy.exp" -Encoding utf8

# 检查expect是否可用
$expectPath = Get-Command expect -ErrorAction SilentlyContinue
if ($expectPath) {
    & expect "$env:TEMP\deploy.exp"
} else {
    Write-Host "expect not found, trying with SSH key setup..."

    # 尝试使用SSH命令直接连接（可能会失败因为需要密码）
    $env:SSH_ASKPASS = "$env:TEMP\deploy_pass.txt"
    $pass | Out-File -FilePath $env:SSH_ASKPASS -Encoding utf8

    # 使用SSH执行命令
    $result = & ssh -o StrictHostKeyChecking=no -o BatchMode=yes -p $port "$user@$server" "mkdir -p /var/www/quiz-system && cd /var/www/quiz-system && rm -rf * && git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git . && ls -la" 2>&1
    Write-Host $result
}

Write-Host "Deployment script created"
