function tree2 {
  $in = $args
  [string]$in = $in
  if ($in -like "*/F*") {$showFiles = "True"; $in = $in.replace(' /F',"")}
  if ($in -like "*/A*") {$showAscii = "True"; $in = $in.replace(' /A',"")}
  [string]$argu = "$in"
  if ($showFiles -eq "True") {
    [string]$argu += " -files"
  }
  if ($showAscii -ne "True") {
    [string]$argu += " -ext"
  }
  $command = "Show-Tree $argu"
  if ($c -notlike "*;*") {iex($command)}
}