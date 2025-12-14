# 업데이트 설치 (대기 중인 업데이트가 있을 경우)
Install-Module PSWindowsUpdate -Force -Confirm:$false
Import-Module PSWindowsUpdate
Get-WindowsUpdate -Install -AcceptAll

# 강제 재부팅
Restart-Computer -Force