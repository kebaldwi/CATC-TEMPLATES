Import-Module GroupPolicy -ErrorAction Stop
$domain = (Get-ADDomain).DNSRoot
$defaultGpoName = "Default Domain Policy"
$gpo = Get-GPO -Name $defaultGpoName -ErrorAction Stop
Write-Host "Editing GPO: $($gpo.DisplayName) ($($gpo.Id)) in domain $domain"

$regPath = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $regPath -ValueName "AEPolicy" -Type DWord -Value 3
Set-GPRegistryValue -Name $defaultGpoName -Key $regPath -ValueName "AutoEnrollEnabled" -Type DWord -Value 1
Write-Host "Auto-Enrollment policy configured in '$defaultGpoName'."

$regPathEP = "HKLM\Software\Policies\Microsoft\Cryptography\Enrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathEP -ValueName "EnableEnrolleePolicy" -Type DWord -Value 1
Set-GPRegistryValue -Name $defaultGpoName -Key $regPathEP -ValueName "PolicyServerUseKerberos" -Type DWord -Value 1

$acrBase = "HKLM\Software\Policies\Microsoft\Cryptography\AutoCertificateRequest"

Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\Computer" -ValueName "TemplateName" -Type String -Value "Computer"
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\Computer" -ValueName "CAName" -Type String -Value ""
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\Computer" -ValueName "MachineKeySet" -Type DWord -Value 4

Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\DomainController" -ValueName "TemplateName" -Type String -Value "DomainController"
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\DomainController" -ValueName "CAName" -Type String -Value ""
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\DomainController" -ValueName "MachineKeySet" -Type DWord -Value 4

Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\EnrollmentAgentComputer" -ValueName "TemplateName" -Type String -Value "EnrollmentAgentComputer"
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\EnrollmentAgentComputer" -ValueName "CAName" -Type String -Value ""
Set-GPRegistryValue -Name $defaultGpoName -Key "$acrBase\EnrollmentAgentComputer" -ValueName "MachineKeySet" -Type DWord -Value 4

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
