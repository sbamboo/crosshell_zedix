# Get runtime input
$file = $args[0]
$globals = $args[1]
$passBackVars = $args[2]
$legacyNames = $args[3]
$allowFuncCalls = $args[4]
$parameter = $args[5..$args.Length]

# handle globals and push to powershell script scope
$globals = $globals.trimend("§¤§")
foreach ($var in $globals.split("§¤§")) {
    $name = $var.split("§")[0]
    $value = $var.split("§")[1]
    if ($name -ne "" -and $value -ne "") {
        Set-Variable -name $name -value $value -scope "Script"
    }
}
# Run legacyNameScript if needed
if ($legacyNames -eq $True) {
    . "$psscriptroot\pwsh_legacyNames.ps1"
}
# Specify path for exports
$script:cs_runtime_loc = "$psscriptroot"
# Run file
if ($passBackVars -eq $False) {
    . $file @parameter
} else {
    . $file @parameter
    "" | out-file "$psscriptroot\exit.empty"
}