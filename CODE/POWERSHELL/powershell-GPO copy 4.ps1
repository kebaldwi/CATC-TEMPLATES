param(
    [string]$Domain = (Get-ADDomain).DNSRoot,
    [switch]$SkipGpupdate
)

Import-Module GroupPolicy -ErrorAction Stop
Import-Module ActiveDirectory -ErrorAction Stop

$ddp = Get-GPO -Name "Default Domain Policy" -Domain $Domain -ErrorAction Stop

$backupPath = Join-Path $env:TEMP ("DDP-Backup-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
New-Item -ItemType Directory -Path $backupPath | Out-Null
Backup-GPO -Guid $ddp.Id -Path $backupPath | Out-Null

$policyPath = "\\$Domain\SYSVOL\$Domain\Policies\{$($ddp.Id)}"
$machineSecDb = Join-Path $policyPath "Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf"
$secEditDir = Split-Path $machineSecDb -Parent
if (-not (Test-Path $secEditDir)) { New-Item -ItemType Directory -Force -Path $secEditDir | Out-Null }

$tempInf = Join-Path $env:TEMP "Enable-CEP-ConfigModel.inf"
@"
[Version]
signature="\$CHICAGO\$"
Revision=1

[Unicode]
Unicode=yes

[System Access]

[Event Audit]

[Privilege Rights]

[Registry Values]
"MACHINE\Software\Policies\Microsoft\Cryptography\PolicyServers\ConfigurationModel"=4,1

[Profile Description]
Description=Enable Certificate Enrollment Policy Configuration Model
"@ | Set-Content -Path $tempInf -Encoding Unicode

$tempSdb = Join-Path $env:TEMP "cep_configmodel.sdb"
if (Test-Path $tempSdb) { Remove-Item $tempSdb -Force }
secedit /import /db $tempSdb /cfg $tempInf /quiet

$mergedInf = Join-Path $env:TEMP "cep_configmodel_merged.inf"
if (Test-Path $mergedInf) { Remove-Item $mergedInf -Force }
secedit /export /db $tempSdb /cfg $mergedInf /quiet

function Merge-RegistryValues {
    param(
        [string]$sourceInf,
        [string]$targetInf
    )
    $src = Get-Content $sourceInf -Raw
    $tgt = (Test-Path $targetInf) ? (Get-Content $targetInf -Raw) : ""
    function Get-RegBlock([string]$text) {
        $pattern = "(?is)\[Registry Values\](.*?)(\r?\n\[|$)"
        $m = [regex]::Match($text, $pattern)
        if ($m.Success) { return $m.Groups[1].Value.Trim("`r`n") } else { return "" }
    }
    $srcReg = Get-RegBlock $src
    if ([string]::IsNullOrWhiteSpace($srcReg)) { throw "No [Registry Values] found in source INF" }
    $tgtReg = Get-RegBlock $tgt
    $toHash = {
        param($block)
        $h = @{}
        foreach ($line in ($block -split "`r?`n")) {
            $line = $line.Trim()
            if ($line -and -not $line.StartsWith(";")) {
                $key = $line.Split("=")[0].Trim('"')
                $h[$key] = $line
            }
        }
        return $h
    }
    $srcH = & $toHash $srcReg
    $tgtH = & $toHash $tgtReg
    foreach ($k in $srcH.Keys) { $tgtH[$k] = $srcH[$k] }
    $newReg = ($tgtH.Values | Sort-Object) -join "`r`n"
    if ($tgt -match "(?is)\[Registry Values\](.*?)(\r?\n\[|$)") {
        $tgt = [regex]::Replace($tgt, "(?is)(\[Registry Values\])(.*?)(\r?\n\[|$)", "`$1`r`n$newReg`r`n`$3")
    } else {
        if (-not [string]::IsNullOrWhiteSpace($tgt)) { $tgt = $tgt.TrimEnd() + "`r`n`r`n" }
        $tgt += "[Registry Values]`r`n$newReg`r`n"
    }
    $tgt
}

$newInf = Merge-RegistryValues -sourceInf $mergedInf -targetInf $machineSecDb
$newInf | Set-Content -Path $machineSecDb -Encoding Unicode

$gptIni = Join-Path $policyPath "gpt.ini"
if (Test-Path $gptIni) {
    $ini = Get-Content $gptIni
    $verLineIdx = $ini.IndexOf($ini | Where-Object { $_ -match "^Version=" })
    if ($verLineIdx -ge 0) {
        $v = [int]($ini[$verLineIdx].Split("=")[1])
        $ini[$verLineIdx] = "Version=$([int]($v + 1))"
        Set-Content -Path $gptIni -Value $ini -Encoding ASCII
    }
}

if (-not $SkipGpupdate) {
    try { Invoke-GPUpdate -All -RandomDelayInMinutes 0 -Force -ErrorAction Stop } catch { }
    Start-Process "cmd.exe" "/c gpupdate /force" -WindowStyle Hidden
}
