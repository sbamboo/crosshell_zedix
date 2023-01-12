<#
  .SYNOPSIS
  Alias to: dashtime.

  
#>
param([Alias("t")][switch]$timeout,[Alias("p")][switch]$pause)
. $psscriptroot\dashtime.ps1 -weekday @PSBoundParameters