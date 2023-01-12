<#
  .SYNOPSIS
  Cmdlet for printing out a square/rectangle of boxchars.
#>
param(
  [alias("w")][int]$width,
  [alias("h")][int]$height,
  
  [switch]$fill
)

if ($fill) {$width = $host.ui.rawui.buffersize.width; $height = $host.ui.rawui.buffersize.height}

$s = "█"*$width
$line = "`n$s"*$height
return $line