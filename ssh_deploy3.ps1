# PowerShell SSH deployment script using .NET SSH library approach
$server = "45.192.97.233"
$port = 22
$user = "root"
$pass = "K4NHWFAPDGsX"

# Create remote commands
$commands = @"
mkdir -p /var/www/quiz-system
cd /var/www/quiz-system
rm -rf *
git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
ls -la
exit
"@

# Create temp script file
$scriptFile = "$env:TEMP\remote_commands.txt"
$commands | Out-File -FilePath $scriptFile -Encoding utf8

Write-Host "Using SSH with password authentication..."

# Start SSH process
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "ssh.exe"
$psi.Arguments = "-o StrictHostKeyChecking=no -o PasswordAuthentication=yes -o BatchMode=no -p $port $user@$server"
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $false

$process = [System.Diagnostics.Process]::Start($psi)

# Wait for connection
Start-Sleep -Seconds 3

if (!$process.HasExited) {
    # Send commands from file
    $cmd = Get-Content $scriptFile -Raw
    $process.StandardInput.WriteLine($cmd)
    $process.StandardInput.Close()
}

# Wait for output
Start-Sleep -Seconds 10

$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()

Write-Host "Output:"
Write-Host $stdout

if ($stderr) {
    Write-Host "Errors:"
    Write-Host $stderr
}

# Cleanup
Remove-Item $scriptFile -ErrorAction SilentlyContinue
