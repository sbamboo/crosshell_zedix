<#
  .SYNOPSIS
  Cmdlet for handling rich prefix. (Needs a nerdfont installed)
#>

param([alias("l")][string]$load,[alias("r")][switch]$reset,[switch]$debug)

#get presets
if (test-path "$psscriptroot\presets.list") {
  $presets_content_local = gc "$psscriptroot\presets.list"
}
$presets_content_online = iwr "https://raw.githubusercontent.com/simonkalmiclaesson/packagehand_repository/main/repository/cmdlet/_private/private_richprefix/presets.list"
if ($presets_content_online[0] -like "*# format*") {
  $presets_content = $presets_content_online -split "`n"
} else {
  $presets_content = $presets_content_local -split "`n"
}

$richprefix = $script:prefix

if ($load) {
  if ($load -ne "0") {
    if ($load -gt ($presets_content.Length -1)) {
      write-host "No preset with index '$load'" -f red
      exit
    } else {
      $richprefix = $presets_content[$load]
    }
  }

  if ($debug) {write-host "$richprefix" -f green}
  #no ' fix
  [string]$richprefixs = $richprefix
  if ($richprefixs[0] -ne "'") {$richprefix = "'" + $richprefix}
  if ($richprefixs[-1] -ne "'") {$richprefix = $richprefix + "'"}

  #load
  CheckAndRun-input "prefix -set $richprefix"
}

if ($reset) {
    CheckAndRun-input "prefix -reset"
}