Import-Module GroupPolicy -ErrorAction Stop
$domain = (Get-ADDomain).DNSRoot
$defaultGpoName = "Default Domain Policy"
$gpo = Get-GPO -Name $defaultGpoName -ErrorAction Stop
Write-Host "Editing GPO: $($gpo.DisplayName) ($($gpo.Id)) in domain $domain"
$regPathAE = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathAE -ValueName "AEPolicy" -Type DWord -Value 3
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathAE -ValueName "AutoEnrollEnabled" -Type DWord -Value 1
$regPathEP = "HKLM\Software\Policies\Microsoft\Cryptography\Enrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathEP -ValueName "PolicyServerUrl" -Type String -Value ""
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathEP -ValueName "PolicyServerUseKerberos" -Type DWord -Value 1
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathEP -ValueName "EnableEnrolleePolicy" -Type DWord -Value 1
$autoReqBase = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutoEnroll"
New-GPRegistryValue -Name $defaultGpoName -Key $autoReqBase -ValueName "Computer" -Type String -Value "1"
New-GPRegistryValue -Name $defaultGpoName -Key $autoReqBase -ValueName "DomainController" -Type String -Value "1"
New-GPRegistryValue -Name $defaultGpoName -Key $autoReqBase -ValueName "EnrollmentAgentComputer" -Type String -Value "1"
Write-Host "Certificate Services Client policies configured in '$defaultGpoName'."
$DCs = (Get-ADDomainController -Filter * | Select-Object -ExpandProperty HostName)
foreach ($dc in $DCs) {
    Write-Host "Triggering gpupdate /force on $dc ..."
    try {
        Invoke-Command -ComputerName $dc -ScriptBlock { gpupdate /force } -ErrorAction Stop
    } catch {
        Write-Warning "Failed to run gpupdate on $dc. Error: $($_.Exception.Message)"
    }
}
Write-Host "Domain controllers refreshed. For clients, run: gpupdate /force"
