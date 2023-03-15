<#
  .SYNOPSIS
  Alias to: dashtime, shows date.

  
#>
param([Alias("t")][switch]$timeout,[Alias("p")][switch]$pause)
. $psscriptroot\dashtime.ps1 -date @PSBoundParameters