Import-Module GroupPolicy -ErrorAction Stop

$domain = (Get-ADDomain).DNSRoot
$gpoName = "Default Domain Policy"




$computerRegPath = "Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Write-Host "Configuring Computer Configuration settings in the $gpoName"

Set-GPPrefRegistryValue -Name $gpoName -Context Computer -Key $computerRegPath -ValueName "PolicyState" -Type DWORD -Value 1
Set-GPPrefRegistryValue -Name $gpoName -Context Computer -Key $computerRegPath -ValueName "AEPolicy" -Type DWORD -Value 2

Set-GPPrefRegistryValue -Name $gpoName -Context Computer -Key $computerRegPath -ValueName "LocalMachineSubmissions" -Type DWORD -Value 1 

$userRegPath = "Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Write-Host "Configuring User Configuration settings in the $gpoName"

Set-GPPrefRegistryValue -Name $gpoName -Context User -Key $userRegPath -ValueName "PolicyState" -Type DWORD -Value 1
Set-GPPrefRegistryValue -Name $gpoName -Context User -Key $userRegPath -ValueName "AEPolicy" -Type DWORD -Value 2

Write-Host "Default Domain Policy configuration complete."
Write-Host "Run 'gpupdate /force' on domain machines to apply the changes immediately."

gpupdate /force
