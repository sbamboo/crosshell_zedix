<#
  .SYNOPSIS
  Fortune for powershell.
#>
return [System.IO.File]::ReadAllText("$psscriptroot\fortune.txt") -replace "`r`n", "`n" -split "`n%`n" | Get-Random