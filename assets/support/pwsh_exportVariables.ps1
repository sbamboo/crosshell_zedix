# Get arguments
[string]$vars = $args[0]
[array]$vars_to_export = $vars.split(",")
# If length is greater then 0 run
if ($vars_to_export.length -gt 0) {
    $string = ""
    # Iterate through variables
    foreach ($var in $vars_to_export) {
        # Check for ! and if exists add to value
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
        # Add parsing elements
        $string += "$name" + "§" + "$value" + "§¤§"
    }
    # Output to file
    $string | out-file "$psscriptroot\passback.vars" | out-null
} else {
    "" | out-file "$psscriptroot\passback.vars" | out-null
}