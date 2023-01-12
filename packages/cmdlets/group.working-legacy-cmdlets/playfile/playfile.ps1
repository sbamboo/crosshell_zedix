<#
  .SYNOPSIS
  Modified playfile function by: Markus Fleschutz.
#>
param($file,$mp3,$m3u)
#Modified TTS function by: Markus Fleschutz.
#Org: https://github.com/hugenda/PowerShell-2/blob/master/Scripts/speak-test.ps1
#Info.link: https://github.com/fleschutz/PowerShell
#

function Speak { param([string]$Text)
	[void]$Voice.speak("$Text")
}
if ($mp3) {
  $curpath = Get-Location
  $filepathns = $file
  $filepathns = $filepathns -replace '(^\s+|\s+$)','' -replace '\s+',' '
  $filepath = Split-Path "$file"
  $file = Split-Path "$file" -leaf
  $filepath = $filepath -replace '(^\s+|\s+$)','' -replace '\s+',' '
  cd $filepath
  $filecont = Get-Content $file
  cd $curpath
    $FullPath = (get-childItem $filepathns).fullname
	$Filename = (get-item "$FullPath").name
    add-type -assemblyName PresentationCore
	$MediaPlayer = new-object System.Windows.Media.MediaPlayer
	do {
		$MediaPlayer.open($FullPath)
		$Milliseconds = $MediaPlayer.NaturalDuration.TimeSpan.TotalMilliseconds
	} until ($Milliseconds)
	[int]$Minutes = $Milliseconds / 60000
	[int]$Seconds = ($Milliseconds / 1000) % 60
	$MediaPlayer.Volume = 1
	$MediaPlayer.play()
	start-sleep -milliseconds $Milliseconds
	$MediaPlayer.stop()
	$MediaPlayer.close()

} elseif ($m3u) {
  $curpath = Get-Location
  $filepath = Split-Path "$file"
  $file = Split-Path "$file" -leaf
  $filepath = $filepath -replace '(^\s+|\s+$)','' -replace '\s+',' '
  cd $filepath
  $filecont = Get-Content $file
  cd $curpath
    $Lines = $filecont
    add-type -assemblyName PresentationCore
	$MediaPlayer = new-object System.Windows.Media.MediaPlayer
    for ([int]$i=0; $i -lt $Lines.Count; $i++) {
		$Line = $Lines[$i]
		if ($Line[0] -eq "#") { continue }
		$FullPath = (get-childItem "$Line").fullname
		$Filename = (get-item "$FullPath").name
		do {
			$MediaPlayer.open("$FullPath")
			$Milliseconds = $MediaPlayer.NaturalDuration.TimeSpan.TotalMilliseconds
		} until ($Milliseconds)
		[int]$Minutes = $Milliseconds / 60000
		[int]$Seconds = ($Milliseconds / 1000) % 60
		$MediaPlayer.Volume = 1
		$MediaPlayer.play()
		start-sleep -milliseconds $Milliseconds
		$MediaPlayer.stop()
		$MediaPlayer.close()
	}
}
