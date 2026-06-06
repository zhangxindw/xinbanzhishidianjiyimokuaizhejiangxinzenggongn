# Simplified SSH deployment with automatic password input
$ErrorActionPreference = "Continue"
$server = "45.192.97.233"
$port = 22
$user = "root"
$pass = "K4NHWFAPDGsX"

Write-Host "========================================="
Write-Host "Starting deployment to $server..."
Write-Host "========================================="

# Remote commands to execute
$remoteCommands = @"
mkdir -p /var/www/quiz-system
cd /var/www/quiz-system
rm -rf *
git clone https://github.com/zhangxindw/xinbanzhishidianjiyimokuai.git .
ls -la
exit
"@

# Create temp batch file
$batchFile = "$env:TEMP\deploy_batch.bat"
$batchContent = @"
@echo off
echo $pass > "$env:TEMP\pass.txt"
type "$env:TEMP\pass.txt" | ssh -o StrictHostKeyChecking=no -p $port $user@$server "$remoteCommands"
del "$env:TEMP\pass.txt"
"@
$batchContent | Out-File -FilePath $batchFile -Encoding ASCII

Write-Host "Executing deployment commands..."
& $batchFile

# Cleanup
Remove-Item $batchFile -ErrorAction SilentlyContinue

Write-Host "========================================="
Write-Host "Deployment initiated!"
Write-Host "========================================="
