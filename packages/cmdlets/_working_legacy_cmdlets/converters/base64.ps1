<#
  .SYNOPSIS
  Cmdlet for converting from and to base64.
#>
param(
  [Parameter(ValueFromPipeline=$true)]
  [string]$in,
  [switch]$encode,
  [switch]$decode
)

if ($encode) {
  return [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($in))
} elseif ($decode) {
  return [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($in))
}