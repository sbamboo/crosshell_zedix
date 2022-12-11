$call_raw = $args
$call = [string]$call_raw
$call | out-file "$psscriptroot\passback.calls" | out-null