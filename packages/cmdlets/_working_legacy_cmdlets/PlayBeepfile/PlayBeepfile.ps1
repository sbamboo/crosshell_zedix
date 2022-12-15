<#
  .SYNOPSIS
  Cmdlet for playing beepfiles.
#>
param($beepfile)
$beepData = gc $beepfile
$beepData = $beepData -replace ',','`n'
foreach ($note in $beepData) {
  $noteArray = $note -split ':'
  $a = $noteArray[0]
  $b = $noteArray[1]
  [console]::beep($a,$b)
}