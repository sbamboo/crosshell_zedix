<#
  .SYNOPSIS
  Cmdlet for converting from and to binary.
#>
param(
  [Parameter(ValueFromPipeline=$true)]
  [string]$in,
  [switch]$encode,
  [switch]$decode
)

if ($encode) {
  [array]$binaryArray = [System.Text.Encoding]::UTF8.GetBytes($in) | %{ [System.Convert]::ToString($_,2).PadLeft(8,'0') }
  [string]$bin = $null
  foreach ($row in $binaryArray) {
    $bin += "$row "
  }
  return [string]$bin.trimEnd(" ")
} else {
  return ($in -split " " | % { [char]([convert]::ToInt32("$_",2)) }) -join ""
}