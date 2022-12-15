<#
  .SYNOPSIS
  Alias to: calc
#>
param(
  [Parameter(ValueFromPipeline=$true)]
  [string]$expression,
  [switch]$mathlibinfo
)

. "$psscriptroot\calc.ps1" @PSBoundParameters -usemathjs