# Configure certificate-related policies in the Default Domain Policy (cisco.com)
# Requires: RSAT Group Policy, domain admin perms (or equivalent)

param(
  [string]$DomainFqdn = "cisco.com",
  [string]$DefaultDomainGpoName = "Default Domain Policy",
  # Path to the root CA certificate in PEM (Base64) format
  [string]$PemPath = "C:\Temp\RootCA.pem"
)

Import-Module GroupPolicy -ErrorAction Stop
Import-Module PKI -ErrorAction SilentlyContinue | Out-Null

# Validate domain context
$domain = (Get-ADDomain -Identity $DomainFqdn -ErrorAction Stop)

# Resolve the Default Domain Policy
$gpo = Get-GPO -Name $DefaultDomainGpoName -Domain $domain.DNSRoot -ErrorAction Stop
Write-Host "Using GPO: $($gpo.DisplayName) in domain $($domain.DNSRoot)"

# ------------------------------------------------------------------------------
# 1) Certificate Services Client – Auto-Enrollment (Computer & User)
#    GUI: Security Settings > Public Key Policies > Certificate Services Client – Auto-Enrollment
#    AEPolicy bitmask: 1=Enable, 2=Renew expired, 4=Update certs from templates. 7 enables all.
# ------------------------------------------------------------------------------

$compAEKey = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compAEKey -ValueName "AEPolicy" -Type DWord -Value 7
# Optional: retry period in hours
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compAEKey -ValueName "AEExpirationPeriod" -Type DWord -Value 8

$userAEKey = "HKCU\Software\Policies\Microsoft\Cryptography\AutoEnrollment"
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userAEKey -ValueName "AEPolicy" -Type DWord -Value 7
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userAEKey -ValueName "AEExpirationPeriod" -Type DWord -Value 8

Write-Host "Enabled Certificate Services Client – Auto-Enrollment (Computer/User)."

# ------------------------------------------------------------------------------
# 2) Certificate Services Client – Certificate Enrollment Policy (CEP)
#    This policy controls AD/HTTP CEP retrieval. Below enables default AD CEP.
#    Computer & User paths are the same hive flavors.
#    Common values:
#      - EnableADCEP = 1 (use Active Directory for policy)
#      - StrongPrivacy = 0/1 (optional)
# ------------------------------------------------------------------------------

$compCEPKey = "HKLM\Software\Policies\Microsoft\Cryptography\PolicyServers"
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compCEPKey -ValueName "EnableADCEP" -Type DWord -Value 1
# Optional privacy preference
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compCEPKey -ValueName "StrongPrivacy" -Type DWord -Value 0

$userCEPKey = "HKCU\Software\Policies\Microsoft\Cryptography\PolicyServers"
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userCEPKey -ValueName "EnableADCEP" -Type DWord -Value 1
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userCEPKey -ValueName "StrongPrivacy" -Type DWord -Value 0

Write-Host "Enabled Certificate Services Client – Certificate Enrollment Policy (AD CEP) (Computer/User)."

# ------------------------------------------------------------------------------
# 3) Certificate Path Validation Settings
#    GUI: Security Settings > Public Key Policies > Certificate Path Validation Settings
#    Below sets common defaults:
#      - Enable user/computer chain policy processing
#      - Revocation checking for end-entity and CA certs
#      - Use machine revocation checking
# ------------------------------------------------------------------------------

# Computer
$compCPV = "HKLM\Software\Policies\Microsoft\SystemCertificates\ChainEngine\Config"
# Enable chain engine policies
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compCPV -ValueName "EnableCSPs" -Type DWord -Value 1 -ErrorAction SilentlyContinue
# Revocation checking flags: 0x00000004 = Check end cert, 0x00000008 = Check chain, 0x00000010 = Check time validity
# Choose 0x0C (12) to check end entity and chain; adjust as needed
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compCPV -ValueName "RevocationCheckFlags" -Type DWord -Value 12
# Use machine revocation
Set-GPRegistryValue -Name $gpo.DisplayName -Key $compCPV -ValueName "UseMachineRevocation" -Type DWord -Value 1

# User
$userCPV = "HKCU\Software\Policies\Microsoft\SystemCertificates\ChainEngine\Config"
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userCPV -ValueName "EnableCSPs" -Type DWord -Value 1 -ErrorAction SilentlyContinue
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userCPV -ValueName "RevocationCheckFlags" -Type DWord -Value 12
Set-GPRegistryValue -Name $gpo.DisplayName -Key $userCPV -ValueName "UseMachineRevocation" -Type DWord -Value 1

Write-Host "Configured Certificate Path Validation Settings (Computer/User)."

# ------------------------------------------------------------------------------
# 4) Automatic Certificate Request Settings (Computer)
#    GUI: Security Settings > Public Key Policies > Automatic Certificate Request Settings
#    This is machine-side only (no user CARs).
#    The classic policy writes into:
#      HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticEnrollment\ 
#    or via Security Templates/INF. Here we populate the legacy CAR list for templates.
#
#    NOTE: Replace the template names below with the exact template display names
#    that exist on your Enterprise CA. Common examples:
#      - "Computer"
#      - "DomainController"
#      - "Enrollment Agent (Computer)"
# ------------------------------------------------------------------------------

$carKey = "HKLM\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticEnrollment"
$carTemplates = @(
  "Computer",
  "DomainController",
  "Enrollment Agent (Computer)"
)

# Store as a REG_MULTI_SZ list under "MachineAutoEnrollmentTemplateList"
# Some environments also use "AutoEnrollmentTemplateList". We'll set both for coverage.
Set-GPRegistryValue -Name $gpo.DisplayName -Key $carKey -ValueName "MachineAutoEnrollmentTemplateList" -Type MultiString -Value $carTemplates
Set-GPRegistryValue -Name $gpo.DisplayName -Key $carKey -ValueName "AutoEnrollmentTemplateList" -Type MultiString -Value $carTemplates

Write-Host "Configured Automatic Certificate Request Settings for: $($carTemplates -join ', ')."

# ------------------------------------------------------------------------------
# 5) Import Root CA PEM into Trusted Root and Trusted Publishers via GPO
#    GUI: Security Settings > Public Key Policies > Trusted Root Certification Authorities / Trusted Publishers
#    Implementation: Define the cert as part of the GPO Machine certificate stores using GptTmpl.inf registry policy.
#    Easiest approach: Import into local machine store on the GPO itself with certutil and write into GPO SYSVOL.
#    We will instead convert PEM -> DER and embed as Registry-based policy for certificate stores with GPMC cmdlets.
#
#    Practical and reliable approach with Group Policy cmdlets:
#      - Convert PEM to CER (DER/Base64) on the admin box
#      - Use certutil to import into the GPO's "Policy" stores by direct registry policy values.
#
#    Below: read PEM, export as .cer, then use the Group Policy "Public Key Policies" special keys to deploy certificate.
# ------------------------------------------------------------------------------

if (-not (Test-Path $PemPath)) {
  throw "PEM file not found at $PemPath"
}

# Convert PEM to CER (Base64 DER) for ease of use
$cerOut = Join-Path $env:TEMP "rootca.cer"
# If PKI module is available, use it; otherwise fallback to certutil
try {
  $certObj = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 (Get-Content -Path $PemPath -Raw)
  [System.IO.File]::WriteAllBytes($cerOut, $certObj.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert))
} catch {
  # Fallback with certutil
  certutil -encode $PemPath $cerOut | Out-Null
  # certutil -encode creates a Base64-encoded file; acceptable for import
}

if (-not (Test-Path $cerOut)) {
  throw "Failed to prepare CER file for import."
}

# Deploy certificates through GPO using the Certificate Store policy registry locations
# Trusted Root Certification Authorities (Machine): HKLM\Software\Policies\Microsoft\SystemCertificates\Root\Certificates\<Thumbprint>\Blob
# Trusted Publishers (Machine):                    HKLM\Software\Policies\Microsoft\SystemCertificates\TrustedPublisher\Certificates\<Thumbprint>\Blob

# Load cert to get thumbprint and raw bytes
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import($cerOut)
$thumb = ($cert.Thumbprint -replace "\s","").ToUpper()
$raw = $cert.RawData

function Set-CertToGpoStore {
  param(
    [string]$GpoName,
    [string]$StoreKeyBase,  # e.g., HKLM\...\Root or HKLM\...\TrustedPublisher
    [string]$Thumbprint,
    [byte[]]$RawBytes
  )
  $certKey = "$StoreKeyBase\Certificates\$Thumbprint"
  # Put entire DER blob into "Blob" value (REG_BINARY)
  Set-GPRegistryValue -Name $GpoName -Key $certKey -ValueName "Blob" -Type Binary -Value $RawBytes
}

$rootStore = "HKLM\Software\Policies\Microsoft\SystemCertificates\Root"
$tpStore   = "HKLM\Software\Policies\Microsoft\SystemCertificates\TrustedPublisher"

Set-CertToGpoStore -GpoName $gpo.DisplayName -StoreKeyBase $rootStore -Thumbprint $thumb -RawBytes $raw
Set-CertToGpoStore -GpoName $gpo.DisplayName -StoreKeyBase $tpStore   -Thumbprint $thumb -RawBytes $raw

Write-Host "Imported root certificate ($thumb) into Trusted Root CA and Trusted Publishers of the GPO."

Write-Host "All requested settings have been configured in the Default Domain Policy."

Write-Host "Next steps:"
Write-Host " - Ensure certificate templates (Computer, DomainController, Enrollment Agent (Computer)) are published on the Enterprise CA and permissions include Autoenroll/Enroll."
Write-Host " - Run 'gpupdate /force' on target machines, or wait for policy refresh."
Write-Host " - Review event logs: Applications and Services Logs > Microsoft > Windows > CertificateServicesClient-*"
