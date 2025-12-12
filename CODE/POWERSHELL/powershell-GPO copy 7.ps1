$GpoName = "Default Domain Policy"
$TemplatesToAdd = @(
    "Enrollment Agent (Computer)",
    "Computer"
)

Import-Module GroupPolicy -ErrorAction Stop
Import-Module ActiveDirectory -ErrorAction Stop

$gpo = Get-GPO -Name $GpoName -ErrorAction Stop
$domain = (Get-ADDomain).DNSRoot
$gpoSysvolPath = "\\$domain\SYSVOL\$domain\Policies\{$($gpo.Id)}\Machine\Microsoft\Windows NT\SecEdit"
$gptPath = Join-Path $gpoSysvolPath "GptTmpl.inf"

if (-not (Test-Path $gpoSysvolPath)) {
    New-Item -Path $gpoSysvolPath -ItemType Directory -Force | Out-Null
}

$existing = @()
if (Test-Path $gptPath) {
    $existing = Get-Content -Path $gptPath -Raw -ErrorAction Stop
}

function Ensure-Section {
    param([string]$content, [string]$sectionName)
    if ($content -notmatch "(?m)^\[$([Regex]::Escape($sectionName))\]\s*$") {
        if ([string]::IsNullOrWhiteSpace($content)) {
            return "[$sectionName]`r`n"
        } else {
            return ($content.TrimEnd() + "`r`n`r`n[$sectionName]`r`n")
        }
    }
    return $content
}

function Set-Version-Section {
    param([string]$content)
    $content = Ensure-Section -content $content -sectionName "Version"
    $lines = $content -split "`r?`n"
    $inVersion = $false
    $updated = @()
    $revisionSet = $false
    $signatureSet = $false
    foreach ($line in $lines) {
        if ($line -match '^\[Version\]\s*$') {
            $inVersion = $true
            $updated += $line
            continue
        }
        if ($inVersion) {
            if ($line -match '^\[') { $inVersion = $false }
            else {
                if ($line -match '^\s*signature\s*=\s*"\$CHICAGO\$"\s*$') { $signatureSet = $true }
                if ($line -match '^\s*Revision\s*=\s*(\d+)\s*$') {
                    $cur = [int]$Matches[1]
                    $line = "Revision=$($cur + 1)"
                    $revisionSet = $true
                }
            }
        }
        $updated += $line
    }
    if (-not $signatureSet -or -not $revisionSet) {
        $pre = ($updated -join "`r`n")
        $pre = [regex]::Replace($pre, '(?ms)^\[Version\]\s*.*?(?=^\[|\Z)', '')
        $versionBlock = @(
            "[Version]",
            'signature="$CHICAGO$"',
            "Revision=1"
        ) -join "`r`n"
        $pre = ($versionBlock + "`r`n`r`n" + $pre.TrimStart())
        return $pre
    } else {
        return ($updated -join "`r`n")
    }
}

function Ensure-Registry-Values-Section {
    param([string]$content)
    $content = Ensure-Section -content $content -sectionName "Registry Values"
    return $content
}

$entries = @()
foreach ($tpl in $TemplatesToAdd) {
    $valueName = ([guid]::NewGuid()).ToString()
    $entries += "`"MACHINE\Software\Policies\Microsoft\Cryptography\AutoEnrollment\AutomaticRequests!$valueName`"=SZ:`"$tpl`""
}

function Upsert-RegistryValues {
    param(
        [string]$content,
        [string[]]$entriesToAdd
    )
    $content = Ensure-Registry-Values-Section -content $content
    $lines = $content -split "`r?`n"
    $out = @()
    $inReg = $false
    foreach ($line in $lines) {
        if ($line -match '^\[Registry Values\]\s*$') { $inReg = $true; $out += $line; continue }
        if ($inReg -and $line -match '^\[') {
            foreach ($e in $entriesToAdd) { $out += $e }
            $inReg = $false
            $out += $line
            continue
        }
        $out += $line
    }
    if ($inReg) {
        foreach ($e in $entriesToAdd) { $out += $e }
        $inReg = $false
    }
    return ($out -join "`r`n")
}

$newContent = $existing
$newContent = Set-Version-Section -content $newContent
$newContent = Upsert-RegistryValues -content $newContent -entriesToAdd $entries

$newContent | Set-Content -Path $gptPath -Encoding Unicode

$gpoRoot = Split-Path -Path $gpoSysvolPath -Parent
$policyRoot = Split-Path -Path $gpoRoot -Parent
$gptIni = Join-Path (Split-Path -Path $policyRoot -Parent) "gpt.ini"

if (Test-Path $gptIni) {
    $ini = Get-Content -Path $gptIni
    $newIni = @()
    $versionIncremented = $false
    foreach ($line in $ini) {
        if ($line -match '^\s*Version\s*=\s*(\d+)\s*$') {
            $newIni += ("Version=" + ([int]$Matches[1] + 1))
            $versionIncremented = $true
        } else {
            $newIni += $line
        }
    }
    if (-not $versionIncremented) {
        $newIni += "Version=1"
    }
    $newIni | Set-Content -Path $gptIni -Encoding ASCII
}

$tempInf = Join-Path $env:TEMP "GptTmpl_$(($gpo.Id).ToString()).inf"
Copy-Item -Path $gptPath -Destination $tempInf -Force

try {
    secedit.exe /configure /db "$env:SystemRoot\security\Database\secedit.sdb" /cfg $tempInf /quiet | Out-Null
} catch {
    Write-Warning "secedit application to local DB failed or not necessary."
}

Write-Host "Done. Review in GPMC and test gpupdate /force on a client."
