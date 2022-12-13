[string]$inp = $args
$c = '"' + $inp + '"' + " | . $PSScriptroot" + "\.lolcat\lolcat.ps1"
iex($c)