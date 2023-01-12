$pa1 = $args[0]
$pa = [string]$pa1
$pa = $pa.trim("'")
$add = ";" + $pa
$curp = $env:Path
$curps = [string]$curp
if ("$curps" -like "*$add*") {echo "Path already added!"} else {
	[Environment]::SetEnvironmentVariable("Path", $env:Path + $add, "User")
}