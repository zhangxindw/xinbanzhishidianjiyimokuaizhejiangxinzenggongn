# 部署脚本 - 使用提供的密码
$server = "45.192.97.233"
$port = 22
$user = "root"
$pass = "K4NHWFAPDGsX"

Write-Host "========================================"
Write-Host "        项目部署脚本"
Write-Host "========================================"
Write-Host ""
Write-Host "服务器: $server"
Write-Host "端口: $port"
Write-Host "用户: $user"
Write-Host ""

Write-Host "正在连接服务器..."

# 创建部署命令（合并为单个命令）
$deployCmd = @"
mkdir -p /var/www/quiz-system && cd /var/www/quiz-system && rm -rf * && git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git . && cd backend && pip3 install flask flask-cors pymysql sqlalchemy python-dotenv xlsxwriter Werkzeug Jinja2 -q && cd ../frontend && npm install && npm run build && echo '部署完成!'
"@

# 使用plink进行连接
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "D:\putty\plink.exe"
$pinfo.Arguments = "-P $port -pw $pass $user@$server `"$deployCmd`""
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $false

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $pinfo
$process.Start() | Out-Null

Write-Host "正在执行部署命令..."

# 获取输出
$output = $process.StandardOutput.ReadToEnd()
$errors = $process.StandardError.ReadToEnd()

$process.WaitForExit()

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

Write-Host ""
Write-Host "部署完成! 退出码: $($process.ExitCode)"
