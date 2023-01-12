[string]$inp = $args
$c = " . $PSScriptroot" + "\Emojis.ps1 " + '"' + $inp + '"'
iex($c)