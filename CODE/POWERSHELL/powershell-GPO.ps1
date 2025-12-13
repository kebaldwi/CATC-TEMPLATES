Import-Module ActiveDirectory -ErrorAction Stop
Import-Module GroupPolicy -ErrorAction Stop

function Get-TemplateGuidByNames {
    param(
        [Parameter(Mandatory)]
        [string[]] $NamesOrCNs
    )
    $configNC = (Get-ADRootDSE).configurationNamingContext
    $baseDN   = "CN=Certificate Templates,CN=Public Key Services,CN=Services,$configNC"
    $all = Get-ADObject -SearchBase $baseDN -LDAPFilter "(objectClass=pKICertificateTemplate)" -Properties displayName, cn, objectGUID
    foreach ($name in $NamesOrCNs) {
        $match = $all | Where-Object { ($_.displayName -eq $name) -or ($_.cn -eq $name) } | Select-Object -First 1
        if ($match) {
            $guid = [System.Guid]$match.ObjectGUID
            return ("{" + $guid.ToString() + "}")
        }
    }
    return $null
}

$DesiredTemplates = @{
    "Computer"                       = @("Computer")
    "Domain Controller"              = @("Domain Controller","DomainController")
    "Enrollment Agent (Computer)"    = @("Enrollment Agent (Computer)","EnrollmentAgentComputer")
}

$resolved = @{}
foreach ($k in $DesiredTemplates.Keys) {
    $guid = Get-TemplateGuidByNames -NamesOrCNs $DesiredTemplates[$k]
    if ($guid) { $resolved[$k] = $guid } else { Write-Warning "Could not find template for '$k' using names: $($DesiredTemplates[$k] -join ', ')" }
}

$missing = $DesiredTemplates.Keys | Where-Object { -not $resolved.ContainsKey($_) }
if ($missing.Count -gt 0) {
    Write-Error ("Missing required template(s): " + ($missing -join ', '))
    return
}

$domain = (Get-ADDomain).DNSRoot
$defaultGpoName = "Default Domain Policy"
$gpo = Get-GPO -Name $defaultGpoName -ErrorAction Stop
Write-Host "Editing GPO: $($gpo.DisplayName) ($($gpo.Id)) in domain $domain"

$regBase    = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
$regAutoReq = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests"

Set-GPRegistryValue -Name $defaultGpoName -Key $regBase -ValueName "AEPolicy" -Type DWord -Value 3
Set-GPRegistryValue -Name $defaultGpoName -Key $regBase -ValueName "AutoEnrollEnabled" -Type DWord -Value 1

Set-GPRegistryValue -Name $defaultGpoName -Key $regAutoReq -ValueName "Computer" -Type String -Value $resolved["Computer"]
Set-GPRegistryValue -Name $defaultGpoName -Key $regAutoReq -ValueName "Domain Controller" -Type String -Value $resolved["Domain Controller"]
Set-GPRegistryValue -Name $defaultGpoName -Key $regAutoReq -ValueName "Enrollment Agent (Computer)" -Type String -Value $resolved["Enrollment Agent (Computer)"]

$resolvedSummary = ($resolved.Keys | Sort-Object | ForEach-Object { "$_=$($resolved[$_])" }) -join '; '
Write-Host "Configured Automatic Certificate Request Settings in '$defaultGpoName'."
Write-Host "Resolved GUIDs: $resolvedSummary"

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
