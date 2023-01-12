<#
  .SYNOPSIS
  prints out our math plan.
#>
param([int]$week,[string]$file,[switch]$table,[string]$day,[Alias("dmode")][switch]$daymode)

. "$psscriptroot\.math_plan_parse\math_plan_read.ps1" @PSBoundParameters