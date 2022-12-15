<#
  .SYNOPSIS
  Modified TTS function by: Markus Fleschutz.
#>
param([Parameter(ValueFromPipeline=$true)]$text,$file,$test)

#Modified TTS function by: Markus Fleschutz.
#Org: https://github.com/hugenda/PowerShell-2/blob/master/Scripts/speak-test.ps1
#Info.link: https://github.com/fleschutz/PowerShell
#

function Speak { param([string]$Text)
	[void]$Voice.speak("$Text")
}
if ($file) {
  $curpath = Get-Location
  $filepath = Split-Path "$file"
  $file = Split-Path "$file" -leaf
  $filepath = $filepath -replace '(^\s+|\s+$)','' -replace '\s+',' '
  cd $filepath
  $Text = Get-Content $file
  cd $curpath
  $Voice = new-object -ComObject SAPI.SPVoice
  $Voice.Speak($Text)
} elseif ($test) {
  Write-Host "Starting speek test..." -b Blue
    $Voice = new-object -ComObject SAPI.SPVoice
	$DefaultVolume = $Voice.volume
	$DefaultRate = $Voice.rate
	Speak("This is the default voice with default volume $DefaultVolume and speed $DefaultRate")

	$Voice.rate = -10
	Speak("Let's speak very, very slow")
	$Voice.rate = -5
	Speak("Let's speak very slow")
	$Voice.rate = -3
	Speak("Let's speak slow")
	$Voice.rate = 0
	Speak("Let's speak normal")
	$Voice.rate = 2
	Speak("Let's speak fast")
	$Voice.rate = 5
	Speak("Let's speak very fast")
	$Voice.rate = 10
	Speak("Let's speak very, very fast")
	$Voice.rate = $DefaultRate

	$Voice.volume = 100
	Speak("Let's try 100% volume")
	$Voice.volume = 75
	Speak("Let's try 75% volume")
	$Voice.volume = 50
	Speak("Let's try 50% volume")
	$Voice.volume = 25
	Speak("Let's try 25% volume")
	$Voice.volume = $DefaultVolume

	$Voices = $Voice.GetVoices()
	foreach ($OtherVoice in $Voices) {
		$Voice.Voice = $OtherVoice
		$Description = $OtherVoice.GetDescription()
		Speak("Hi, I'm the voice called $Description")
	}
    Write-Host "Done!" -b Blue
    pause
} else {
  Speak("$text")
}

