<#
  .SYNOPSIS
  Converts dictionaries.
#>
param($in,$out,$logout)
  if ($logout) {$logn = $logout} else {$logn = "ConvertDictionary.log"}
  $newDictionary = $null
  $counter = $null
  $dictionary = get-content "$in"
  foreach ($_ in $dictionary) {
    [array]$wordArray = $_ -split '/'
    $splitWord = $wordArray[0]
    $newDictionary += "`n$splitWord"
    $counter++
    $curword = $_
    echo "$counter/$dicLength,  $curword ==> $splitWord"
    if ($script:ConvertDictionary_printLog) {"$counter/$dicLength,  $curword ==> $splitWord" | out-file -file $logn -append}
  }
  $newDictionary | out-file -file $out