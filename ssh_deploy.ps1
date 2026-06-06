$pass = "K4NHWFAPDGsX"
$server = "45.192.97.233"
$port = 22
$user = "root"

# 使用SSH命令执行部署
$cmd = @"
mkdir -p /var/www/quiz-system
cd /var/www/quiz-system
rm -rf *
git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
exit
"@

# 启动进程并发送密码
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "ssh"
$pinfo.Arguments = "-o StrictHostKeyChecking=no -o BatchMode=yes -p $port $user@$server '$cmd'"
$pinfo.RedirectStandardInput = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $false

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start()

# 等待连接建立
Start-Sleep -Seconds 3

# 发送密码（如果需要）
if (!$p.HasExited) {
    $p.StandardInput.WriteLine($pass)
    $p.StandardInput.Flush()
}

# 获取输出
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()

Write-Host "STDOUT: $stdout"
Write-Host "STDERR: $stderr"

$p.WaitForExit()
Write-Host "Exit code: $($p.ExitCode)"
