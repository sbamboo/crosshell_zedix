<#
  .SYNOPSIS
  Tool for local networks on the computer.
#>

param([switch]$debug,[switch]$exitonend,[switch]$ranged)

$title = "WifiMan 1.0 (XXXXXXXXX-00-X0)"
$desc = "Tool to for WIFI networks on your device."
$bar = "##########################################"

#settings
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
    if ($ranged -eq $True) {
      $script:tmp = netsh wlan show networks; foreach ($i in $tmp) { if($i -like "*:*") {$i = $i -Split ":"; $i = $i[1]; $i = $i.TrimStart(" "); write-host $i -b darkblue -f white}}
      $tmp = ""
    } else {
      $script:tmp = netsh wlan show profile; foreach ($i in $tmp) { if($i -like "*:*") {$i = $i -Split ":"; $i = $i[1]; $i = $i.TrimStart(" "); write-host $i -b darkblue -f white}}
      $tmp = ""
    }
  write-host ""
  write-host "$bar" -f darkgreen
  write-host "PSW: Passwords, CNC: Connect, 'exit': Exits takes no network"
  $network = Read-host "Write an action followed by the network (<action>:<network>)"
  if ($network -eq "exit") {break}
  $action = ($network.Split(":"))[0]
  $network = ($network.Split(":"))[1]
  if ($action -eq "PSW") {
    write-host "You will see sensitive info like passwords for WIFI, please check that you dont share your screen and input key:"
    $keyin = Read-host "key"
    if ($keyin -eq "exit") {break}
    if ($keyin -eq "$key") {
      $script:tmp = netsh wlan show profile "$network" key=clear; foreach ($i in $tmp) { if($i -like "*key content*") {$i = $i -Split ":"; $i = $i[1]; $i = $i.TrimStart(" "); write-host -nonewline "Password for $network : "; write-host "$i" -b green -f black}}; pause
      $tmp = ""
    }
  } elseif ($action -eq "CNC") {
    $script:tmp = netsh wlan connect name="$network"
    write-host $tmp
    Pause
  }
  if ($exitonend -eq "true") {break}
}