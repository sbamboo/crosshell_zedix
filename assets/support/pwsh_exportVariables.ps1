[string]$vars = $args[0]
[array]$vars_to_export = $vars.split(",")
if ($vars_to_export.length -gt 0) {
    $string = ""
    foreach ($var in $vars_to_export) {
        if ([string]$var[0] -eq "!") {
            $var = $var.trimstart("!")
            $value = get-variable "$var" -ValueOnly
            $var = "!" + $var
        } else {
            $value = get-variable "$var" -ValueOnly
        }
        $name = $var
        # Handle non string vars
        if ($value -is [array]) {
            $str = "["
            foreach ($sv in $value) {
                $str += "'" + $sv + "',"
            }
            [string]$value = $str + "]"
        }
        $string += "$name" + "§" + "$value" + "§¤§"
    }
    $string | out-file "$psscriptroot\passback.vars" | out-null
} else {
    "" | out-file "$psscriptroot\passback.vars" | out-null
}