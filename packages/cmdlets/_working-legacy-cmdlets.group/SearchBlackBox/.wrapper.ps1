[string]$inp = $args
$c = " . $PSScriptroot" + "\SearchBlackBox.ps1 " + '"' + $inp + '"'
iex($c)