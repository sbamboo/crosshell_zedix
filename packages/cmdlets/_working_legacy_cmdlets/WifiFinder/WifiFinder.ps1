<#
  .SYNOPSIS
  Shows passwords for local networks on the computer.
#>

$title = "Wifi Finder 2.0 (jdqw1923k-01-g2)"
$desc = "Tool to view info about WIFI networks on your device."
$bar = "#######################################################"

#settings
param ([switch]$debug,[switch]$exitonend)
$debug = "false"
$exitonend = "false"
$intkey = "101"

#getkey
$keyexi = Test-path "wififinder.key"
if ($keyexi -eq "True") {
 $key = Get-Content "wififinder.key"
} else {
 $key = "$intkey"
}

while ("1" -eq "1") {
  $host.ui.RawUI.WindowTitle = "$title"
  cls
  write-host "$title"
  write-host "($desc)"
  write-host "$bar" -f darkgreen
  write-host "WIFI Networks stored on this device:"
    $script:tmp = netsh wlan show profile; foreach ($i in $tmp) { if($i -like "*:*") {$i = $i -Split ":"; $i = $i[1]; $i = $i.TrimStart(" "); write-host $i -b darkblue -f white}}
    $tmp = ""
  write-host ""
  write-host "$bar" -f darkgreen
  $network = Read-host "Choose a Network to view info off"
  if ($network -eq "exit") {break}
  write-host "You will see sensitive info like passwords for WIFI, please check that you dont share your screen and input key:"
  $keyin = Read-host "key"
  if ($keyin -eq "exit") {break}
  if ($keyin -eq "$key") {
    $script:tmp = netsh wlan show profile "$network" key=clear; foreach ($i in $tmp) { if($i -like "*key content*") {$i = $i -Split ":"; $i = $i[1]; $i = $i.TrimStart(" "); write-host -nonewline "Password for $network : "; write-host "$i" -b green -f black}}; pause
    $tmp = ""
  }
  if ($exitonend -eq "true") {break}
}