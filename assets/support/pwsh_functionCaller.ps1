# Get arguments
$call_raw = $args[0]
$opt = $args[1]
$call = [string]$call_raw
# if encode param encode
if ($opt -like "*encode*") {
    $call = $call -replace '"',"{%2%}"
    $call = $call -replace "'","{%1%}"
}
# Output to file
$call | out-file "$psscriptroot\passback.calls" | out-null