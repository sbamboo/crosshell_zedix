<#
  .SYNOPSIS
  Import of Ma Bingyao's lolcat module.
#>
param(
  [string[]]$Path,
  [Alias('p')]
  [double]$Spread = 3.0,
  [Alias('f')]
  [double]$Freq = 0.1,
  [Alias('i')]
  [int32]$Seed = 0,
  [Alias('a')]
  [switch]$Animate,
  [Alias('d')]
  [int32]$Duration = 12,
  [Alias('s')]
  [double]$Speed = 20.0,
  [Alias('k')]
  [switch]$Keep,
  [Alias('v')]
  [switch]$Version,
  [Alias('h')]
  [switch]$Help
)
$null = $PSBoundParameters.Remove('Path');
$null = $PSBoundParameters.Remove('Keep');
$null = $PSBoundParameters.Remove('Version');
$null = $PSBoundParameters.Remove('Help');

Import-module -force $psscriptroot\lolcat.psm1
Import-module -force $psscriptroot\out-rainbow.psm1
Import-module -force $psscriptroot\out-stripansi.psm1
$inp = $Input
$inp | lolcat @PSBoundParameters