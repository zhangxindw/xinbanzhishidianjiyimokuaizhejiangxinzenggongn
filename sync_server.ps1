$env:SSH_ASKPASS_REQUIRE = "never"
$password = "6dwic8N532a7" | ConvertTo-SecureString -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential("root@154.201.94.140", $password)

Write-Host "正在连接服务器..."
$sshSession = New-PSSession -ComputerName "154.201.94.140" -Credential $credential -Port 22

if ($sshSession) {
    Write-Host "连接成功，正在拉取代码..."
    Invoke-Command -Session $sshSession -ScriptBlock {
        Set-Location "C:\root\xinbanzhishidianjiyimokuaizhejiang"
        git pull new_origin main
        Write-Host "代码同步完成！"
    }
    Remove-PSSession $sshSession
} else {
    Write-Host "连接失败，请检查网络和凭据"
}
