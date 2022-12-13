[string]$inp = $args
$c = '"' + $inp + '"' + " | . $PSScriptroot" + "\lolcat.ps1"
iex($c)