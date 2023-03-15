<#
  .SYNOPSIS
  Alias to: dashtime, shows week.
#>
param([Alias("t")][switch]$timeout,[Alias("p")][switch]$pause)
. $psscriptroot\dashtime.ps1 -week @PSBoundParameters