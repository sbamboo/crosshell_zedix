<#
  .SYNOPSIS
  Prints out a directory tree, use param -f for files and -e for unicode.
#>
. $psscriptroot\.assets\Show-Tree.ps1
. $psscriptroot\.assets\Tree_legacyFormat.ps1
. $psscriptroot\.assets\Tree_Char2_Addon.ps1


$c = "Show-Tree $args"
if ($c -notlike "*;*") {iex($c)}