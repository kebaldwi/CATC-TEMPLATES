Import-Module GroupPolicy -ErrorAction Stop
Import-Module ActiveDirectory -ErrorAction Stop

$domain = (Get-ADDomain).DNSRoot
$defaultGpoName = "Default Domain Policy"

$gpo = Get-GPO -Name $defaultGpoName -ErrorAction Stop
Write-Host "Editing GPO: $($gpo.DisplayName) ($($gpo.Id)) in domain $domain"

$autoEnrollRegPath = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $autoEnrollRegPath -ValueName "AEPolicy" -Type DWord -Value 3
Set-GPRegistryValue -Name $defaultGpoName -Key $autoEnrollRegPath -ValueName "AutoEnrollEnabled" -Type DWord -Value 1

Write-Host "Auto-Enrollment policy configured in '$defaultGpoName'."

$policyBase = "HKLM\Software\Policies\Microsoft\Cryptography\PolicyServers"
Set-GPRegistryValue -Name $defaultGpoName -Key $policyBase -ValueName "Enabled" -Type DWord -Value 1
Set-GPRegistryValue -Name $defaultGpoName -Key $policyBase -ValueName "ADPolicyEnabled" -Type DWord -Value 1

Write-Host "Certificate Services Client - Certificate Enrollment Policy set to Enabled (Active Directory policy)."

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
