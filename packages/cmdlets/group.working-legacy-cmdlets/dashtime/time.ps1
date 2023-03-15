<#
  .SYNOPSIS
  Alias to: dashtime, shows time.
#>
param([Alias("t")][switch]$timeout,[Alias("p")][switch]$pause)
. $psscriptroot\dashtime.ps1 @PSBoundParameters