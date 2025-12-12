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

$adUri = "ldap:///CN=Configuration," + (Get-ADRootDSE).configurationNamingContext
$entryGuid = [guid]::NewGuid().ToString("B")
$entryKey = "$policyBase\$entryGuid"
Set-GPRegistryValue -Name $defaultGpoName -Key $entryKey -ValueName "Url" -Type String -Value $adUri
Set-GPRegistryValue -Name $defaultGpoName -Key $entryKey -ValueName "FriendlyName" -Type String -Value "Active Directory Enrollment Policy"
Set-GPRegistryValue -Name $defaultGpoName -Key $entryKey -ValueName "AuthType" -Type DWord -Value 0
Set-GPRegistryValue -Name $defaultGpoName -Key $entryKey -ValueName "ValidateServer" -Type DWord -Value 1
Set-GPRegistryValue -Name $defaultGpoName -Key $entryKey -ValueName "Priority" -Type DWord -Value 10
Set-GPRegistryValue -Name $defaultGpoName -Key $policyBase -ValueName "Default" -Type String -Value $entryGuid

Write-Host "Certificate Services Client - Certificate Enrollment Policy set to Enabled (Active Directory policy, list updated)."

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
