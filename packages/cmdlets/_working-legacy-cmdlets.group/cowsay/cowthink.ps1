<#
  .SYNOPSIS
  Luke Sampson's pwsh port of cowsay, but thinking.
#>
$cowsay = "$psscriptroot\cowsay.ps1"
if($myinvocation.expectingInput) { $input | & $cowsay @args } else { & $cowsay @args }