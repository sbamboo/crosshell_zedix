<#
  .SYNOPSIS
  Cmdlet for getting information from crosshell webinfo (webi)
#>
param([string]$id,[string]$nid,[alias("o")][switch]$open,[switch]$list)

#Sets
function script:Test-Network { if ($IsWindows) {if (Get-NetAdapter | Where Status -eq "Up") {return $true} else {return $false}}}
$script:Shell_NetworkAvaliable = Test-Network
function script:INeedNetwork {
  if ($script:Shell_NetworkAvaliable -eq $false) {
    write-host "This command needs network access to work!" -f red
    exit
  }
}

# I Need Network
INeedNetwork

#list
if ($list) {
  [string]$id_linkbase = "https://simonkalmiclaesson.github.io/"
  $id_link1 = "websa/shortener.html"
  $url = "$id_linkbase" + "$id_link1" + "?list"
  $c = "id_shorteners = "
  $rawlist = (((iwr "$url").content -split "$c")[1] -split "`n")[0] -replace '"',''
  $rawlist = $rawlist.replace(" ","")
  [array]$webiItems = $rawlist.split(",")
  write-host "Avaliable shortener ids: "
  foreach ($item in $webiItems) {
    write-host $item -f DarkYellow
  }
}

#id
if ($id) {
    [string]$id_linkbase = "https://simonkalmiclaesson.github.io/"
    $id_link1 = "websa/shortener.html"
    $url = "$id_linkbase" + "$id_link1" + "?id=$id&giveurl"
    if ($open) {
      start "$url"
    } else {
      $c = "urllocation_" + "$id" + " = "
      $newlink = (((iwr "$url").content -split "$c")[1] -split "`n")[0] -replace '"',''
      $url = "$id_linkbase" + "$newlink"
      if ($url -eq $id_linkbase) {
        return "`e[31mId '$id' not found online. Try 'webi -list'`e[0m"
      }
      [string]$content = (iwr "$url").content
      $matches = [regex]::matches($content,'<h1>.*</h1>|<p>.*</p>|<i>.*</i>|<br>|<h3>.*</h3>|<b>.*</b>').value
      foreach ($m in $matches) {
        [string]$s = "$m"
        $s = $s.replace("<i>","$($psstyle.Italic)")
        $s = $s.replace("</i>","$($psstyle.ItalicOff)")
        $s = $s.replace("<b>","$($psstyle.Bold)")
        $s = $s.replace("</b>","$($psstyle.BoldOff)")
        $s = $s.replace("<h3>","$($psstyle.Bold)")
        $s = $s.replace("</h3>","$($psstyle.BoldOff)")
        $s = $s.replace("<h1>","$($psstyle.Bold)Article: ")
        $s = $s.replace("</h1>","$($psstyle.BoldOff)")
        $s = $s.replace("<p>","")
        $s = $s.replace("</p>","")
        $s = $s.replace("<br>","")
        write-output "$s"
      }
    }
}

#nid
if ($nid) {
  [string]$nid_linkbase = "https://simonkalmiclaesson.github.io/"
  $nid_link1 = "crosshell_web/idsystem/id_handler.html"
  $url = "$nid_linkbase" + "$nid_link1" + "?id=$nid&giveurl"
  if ($open) {
    start "$url"
  } else {
    $c = "urllocation_" + "$nid" + " = "
    $newlink = (((iwr "$url").content -split "$c")[1] -split "`n")[0] -replace '"',''
    $url = "$nid_linkbase" + "$newlink"
    [string]$content = (iwr "$url").content
    $matches = [regex]::matches($content,'<h1>.*</h1>|<p>.*</p>|<i>.*</i>|<br>').value
    foreach ($m in $matches) {
      [string]$s = "$m"
      $s = $s.replace("<i>","$($psstyle.Italic)")
      $s = $s.replace("</i>","$($psstyle.ItalicOff)")
      $s = $s.replace("<b>","$($psstyle.Bold)")
      $s = $s.replace("</b>","$($psstyle.BoldOff)")
      $s = $s.replace("<h1>","$($psstyle.Bold)Article: ")
      $s = $s.replace("</h1>","$($psstyle.BoldOff)")
      $s = $s.replace("<p>","")
      $s = $s.replace("</p>","")
      $s = $s.replace("<br>","")
      write-output "$s"
    }
  }
}