# PowerShell expect-like script for SSH deployment
$server = "45.192.97.233"
$port = 22
$user = "root"
$pass = "K4NHWFAPDGsX"

# Create a temp script file
$scriptContent = @"
mkdir -p /var/www/quiz-system
cd /var/www/quiz-system
rm -rf *
git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
cd backend
pip3 install flask flask-cors pymysql sqlalchemy python-dotenv xlsxwriter Werkzeug Jinja2
cd ../frontend
npm install
npm run build
exit
"@

# Save script to temp file
$scriptFile = "$env:TEMP\remote_commands.sh"
$scriptContent | Out-File -FilePath $scriptFile -Encoding utf8

# Use plink with password from stdin (via echo)
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = "plink.exe"
$pinfo.Arguments = "-batch -P $port $user@$server -m $scriptFile"
$pinfo.RedirectStandardInput = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $false
$pinfo.WorkingDirectory = "D:\putty"

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$started = $p.Start()

# Wait for password prompt
Start-Sleep -Seconds 2

if (!$p.HasExited) {
    # Send password
    $p.StandardInput.WriteLine($pass)
    $p.StandardInput.Close()
}

# Get output
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()

Write-Host "STDOUT:"
Write-Host $stdout
Write-Host "STDERR:"
Write-Host $stderr
Write-Host "Exit code: $($p.ExitCode)"

# Cleanup
Remove-Item $scriptFile -ErrorAction SilentlyContinue
