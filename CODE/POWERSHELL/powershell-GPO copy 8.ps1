$GpoName              = "PKI - Automatic Certificate Requests"
$LinkToTarget         = "DC=yourdomain,DC=com"
$LinkEnforced         = $false
$ComputerGuid         = "{11111111-1111-1111-1111-111111111111}"
$DCGuid               = "{22222222-2222-2222-2222-222222222222}"
$EAComputerGuid       = "{33333333-3333-3333-3333-333333333333}"

$RegBasePath = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests"

if (-not (Get-Module -ListAvailable -Name GroupPolicy)) {
    Write-Error "GroupPolicy module not found. Install RSAT Group Policy Management Tools."
    return
}

Import-Module GroupPolicy -ErrorAction Stop

$gpo = Get-GPO -Name $GpoName -ErrorAction SilentlyContinue
if (-not $gpo) {
    $gpo = New-GPO -Name $GpoName
}

$existingLinks = (Get-GPOLink -Target $LinkToTarget -ErrorAction SilentlyContinue) | Where-Object { $_.DisplayName -eq $GpoName }
if (-not $existingLinks) {
    New-GPLink -Name $GpoName -Target $LinkToTarget -Enforced:$LinkEnforced | Out-Null
}

function Set-GPPRegistryValue {
    param(
        [Parameter(Mandatory)]
        [string] $GpoName,
        [Parameter(Mandatory)]
        [ValidateSet("HKLM","HKCU")]
        [string] $Hive,
        [Parameter(Mandatory)]
        [string] $KeyPath,
        [Parameter(Mandatory)]
        [string] $ValueName,
        [Parameter(Mandatory)]
        [string] $ValueData,
        [ValidateSet("String","ExpandString","DWord","QWord","Binary","MultiString")]
        [string] $ValueType = "String",
        [ValidateSet("Update","Create","Replace")]
        [string] $Action = "Update"
    )
    Set-GPRegistryValue -Name $GpoName `
        -Key ("{0}\{1}" -f $Hive, $KeyPath) `
        -ValueName $ValueName `
        -Type String `
        -Value $ValueData | Out-Null
}

$valuesToSet = @(
    @{ Name = "Computer";                       Guid = $ComputerGuid },
    @{ Name = "Domain Controller";              Guid = $DCGuid },
    @{ Name = "Enrollment Agent (Computer)";    Guid = $EAComputerGuid }
)

foreach ($v in $valuesToSet) {
    Set-GPRegistryValue -Name $GpoName `
        -Key "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests" `
        -ValueName $v.Name `
        -Type String `
        -Value $v.Guid | Out-Null
}

try {
    New-Item -Path "Registry::HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment" -ErrorAction SilentlyContinue | Out-Null
    New-Item -Path "Registry::HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests" -ErrorAction SilentlyContinue | Out-Null

    New-ItemProperty -Path "Registry::HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests" -Name "Computer" -Value $ComputerGuid -PropertyType String -Force | Out-Null
    New-ItemProperty -Path "Registry::HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests" -Name "Domain Controller" -Value $DCGuid -PropertyType String -Force | Out-Null
    New-ItemProperty -Path "Registry::HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests" -Name "Enrollment Agent (Computer)" -Value $EAComputerGuid -PropertyType String -Force | Out-Null
} catch {
    Write-Warning "Could not write local registry test entries: $($_.Exception.Message)"
}
