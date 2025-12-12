Import-Module GroupPolicy -ErrorAction Stop

$DomainName = (Get-ADDomain).DNSRoot
$GpoName    = "Default Domain Policy"

$TemplatesToAdd = @(
    "Enrollment Agent (Computer)",
    "Computer"
)

$gpo = Get-GPO -Name $GpoName -ErrorAction Stop

function Add-AutoCertRequestForTemplate {
    param(
        [Parameter(Mandatory)]
        [string]$TemplateDisplayName,
        [Parameter(Mandatory)]
        [Microsoft.GroupPolicy.Gpo]$Gpo
    )

    $PolicyKeyPath = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests"
    $ValueName = ([System.Guid]::NewGuid()).ToString()

    Set-GPRegistryValue -Name $Gpo.DisplayName `
        -Key $PolicyKeyPath `
        -Type String `
        -ValueName $ValueName `
        -Value $TemplateDisplayName
}

foreach ($tpl in $TemplatesToAdd) {
    Add-AutoCertRequestForTemplate -TemplateDisplayName $tpl -Gpo $gpo
}

Write-Host "Automatic Certificate Request Settings updated in '$GpoName'."

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
