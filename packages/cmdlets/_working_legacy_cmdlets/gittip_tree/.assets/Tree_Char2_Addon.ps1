function script:Tree2 {
    Set-Alias wh Write-host
    if ($args -like "-help") {
        wh "Tree2 is a script based addon for the Show-Tree function from: https://raw.githubusercontent.com/jdhitsolutions/PSScriptTools/master/functions/ShowTree.ps1"
        wh "This script is made by: Simon Kalmi Claesson"
        pause
        break
    }
    [array]$script:out_tree = ""
    $in = $args
    [string]$in = $in
    if ($in -like "*-Char2*") {
        $in = $in.replace("-Char2","")
        [array]$tmp = Show-Tree $in -showitem -InColor
        foreach ($item in $tmp) {
          $item = $item.replace("+","├")
          $item = $item.replace("|","│")
          $item = $item.replace("-","─")
          if ($item -notlike "*:*") {$item = $item.replace("\","└")}
          [array]$script:out_tree += $item
        }
    } else {
      [array]$script:out_tree = Show-Tree $in -showitem
    }
	return $out_tree
}