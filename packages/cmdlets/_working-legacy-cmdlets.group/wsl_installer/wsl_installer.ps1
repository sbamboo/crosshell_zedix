<#
  .SYNOPSIS
  Cmdlet for installing wsl.
#>
$old_windowtitle = $host.UI.RawUI.WindowTitle
$host.UI.RawUI.WindowTitle = "WSL-Install-Assistant -Ubuntu -BundlePwsh"

function end {$host.UI.RawUI.WindowTitle = $old_windowtitle}

$wslpacklink = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"

#Handle JsonConfig
 $json = (gc ".\WSL_Install_Config.json" | out-string)

 $data = ConvertFrom-Json $json
 $CompatabilityMode = $data.config.compatabilitymode

#Install WSL
if ($CompatabilityMode -eq "Default") {
  #Default
   wsl --Install
   end

} else {
  #Support
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   curl -s -l -o "wsl_update_x64.msi" "$wslpacklink" 
   wsl_update_x64.msi
   wsl --set-default-version 
   
   cls
   echo Now go to Ms-Store and download your desired distro. (ex: Ubuntu 20.4 LTS)
   Write-Host "Then go back here to setup the bundle" -b Darkred
   pause
   end
}

#Setup Bundle
  wsl sudo apt-get update
  wsl sudo apt-get install -y wget apt-transport-https software-properties-common
  wsl wget -q $runtimeurllinux
  wsl sudo dpkg -i packages-microsoft-prod.deb
  wsl sudo apt-get update
  wsl sudo apt-get install -y powershell

  pause
  end