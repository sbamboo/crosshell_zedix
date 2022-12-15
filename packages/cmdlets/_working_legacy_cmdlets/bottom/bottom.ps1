<#
  .SYNOPSIS
  Copy of ClementTsang's Bottom systemviewer.
#>
$curdir = get-location
cd "$psscriptroot\.bottom"
. .\btm.exe $args
cd $curdir