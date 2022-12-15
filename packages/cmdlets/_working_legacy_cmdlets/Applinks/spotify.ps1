<#
  .SYNOPSIS
  Starts spotify if installed in the roaming dir.
#>

$path = "C:\Users\$env:username\AppData\Roaming\Spotify\Spotify.exe"


$old_ErrorActionPreference = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'


$res = test-path $path
if ($res) {start $path}


$ErrorActionPreference = $old_ErrorActionPreference