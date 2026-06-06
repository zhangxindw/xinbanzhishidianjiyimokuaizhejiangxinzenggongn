# 交互式部署脚本
$server = "45.192.97.233"
$port = 22
$user = "root"

Write-Host "========================================"
Write-Host "        项目部署脚本"
Write-Host "========================================"
Write-Host ""
Write-Host "服务器: $server"
Write-Host "端口: $port"
Write-Host "用户: $user"
Write-Host ""

# 获取密码
$pass = Read-Host "请输入服务器密码" -AsSecureString
$plainPass = [System.Net.NetworkCredential]::new("", $pass).Password

Write-Host ""
Write-Host "正在连接服务器..."

# 创建部署命令
$commands = @(
    "mkdir -p /var/www/quiz-system",
    "cd /var/www/quiz-system",
    "rm -rf *",
    "git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .",
    "echo '代码克隆完成'",
    "cd /var/www/quiz-system/backend",
    "pip3 install flask flask-cors pymysql sqlalchemy python-dotenv xlsxwriter Werkzeug Jinja2 2>/dev/null",
    "echo '后端依赖安装完成'",
    "cd /var/www/quiz-system/frontend",
    "npm install",
    "npm run build",
    "echo '前端构建完成'",
    "echo '部署成功!'"
)

# 使用plink进行交互式连接
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "D:\putty\plink.exe"
$pinfo.Arguments = "-P $port $user@$server"
$pinfo.RedirectStandardInput = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $pinfo
$process.Start() | Out-Null

# 等待连接并发送密码
Start-Sleep -Seconds 2
$process.StandardInput.WriteLine($plainPass)

# 发送部署命令
foreach ($cmd in $commands) {
    $process.StandardInput.WriteLine($cmd)
    Start-Sleep -Seconds 1
}

# 等待命令执行
Start-Sleep -Seconds 30

# 获取输出
$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()

Write-Host ""
Write-Host "========================================"
Write-Host "部署输出:"
Write-Host "========================================"
Write-Host $output

if ($errors) {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "错误信息:"
    Write-Host "========================================"
    Write-Host $errors
}

$process.WaitForExit()
Write-Host ""
Write-Host "部署完成! 退出码: $($process.ExitCode)"
