# Gamehub saveserice written by Simon Kalmi Claesson
# 
# Obs! This script should only be used through the gamehub api.
#

param([string]$loc,[string]$datafile)

$Host.UI.RawUI.WindowTitle = "Gamehub SaveService"
[console]::WindowHeight = 15
[console]::WindowWidth = 60


. "$psscriptroot\gamehub_api.ps1"

Set-Location $loc
$file = "$datafile"
$efile = "$psscriptroot\exit.state"

write-host "[Debug] Started listener in $file" -f darkgray

$loop = $true
[int]$lastScore = 0
$user = ""
write-host "Waiting for tmp file..." -f darkgray
while ((test-path "$file") -eq $false) {}
write-host "Continuing!" -f darkgray
if (test-path "$file") {
  $scoreData = get-content "$file"
  [array]$scoreDataA = $scoreData -split ' : '
  $user = $scoreDataA[0]
}
[int]$lastScore = gamehub_userScore -game "snake" -user "$user" -get
#write-host "$lastScore $user"
if (test-path "$efile") {remove-item "$efile" -force}
while ($loop) {
  if (test-path "$efile") {
    if (test-path "$file") {remove-item "$file" -force}
    remove-item "$efile" -force
    $loop = $false
    break
  }
  if (test-path "$file") {
    $scoreData = get-content "$file"
    [array]$scoreDataA = $scoreData -split ' : '
    $user = $scoreDataA[0]
    [int]$newScore = $scoreDataA[-1]
    if ($newScore -gt $lastScore) {
      #write-host "$lastScore"
      $ans = gamehub_userScore -game "snake" -user "$user" -score "$newScore" -update
      #$lastScore = $newScore
      write-host "[Debug] Wrote new score '$newScore' for user '$user'" -f yellow
    }
  }
}