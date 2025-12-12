Import-Module GroupPolicy -ErrorAction Stop
$domain = (Get-ADDomain).DNSRoot
$defaultGpoName = "Default Domain Policy"
$gpo = Get-GPO -Name $defaultGpoName -ErrorAction Stop
Write-Host "Editing GPO: $($gpo.DisplayName) ($($gpo.Id)) in domain $domain"
$regPath = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $defaultGpoName -Key $regPath -ValueName "AEPolicy" -Type DWord -Value 3
Set-GPRegistryValue -Name $defaultGpoName -Key $regPath -ValueName "AutoEnrollEnabled" -Type DWord -Value 1
Write-Host "Auto-Enrollment policy configured in '$defaultGpoName'."
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
