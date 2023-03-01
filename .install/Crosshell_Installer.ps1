# Save data
$old_windowtitle = $host.ui.rawui.windowtitle
$host.ui.rawui.windowtitle = "Crosshell Install Script (1.0)"
$old_dir = Get-Location

# write info
write-host "Crosshell installer script, proceeding..." -f yellow

# Get user name and computer name
$computer_name = $env:computername
$user_name = $env:UserName
$user_domain = $env:UserDomain
write-host "UserName" -f blue -nonewline
write-host ":     " -nonewline
write-host "$user_name" -f yellow
write-host "UserDomain" -f blue -nonewline
write-host ":   " -nonewline
write-host "$user_domain" -f yellow
write-host "ComputerName" -f blue -nonewline
write-host ": " -nonewline
write-host "$computer_name"-f yellow

# Define functions
function GoFolder {
  param([string]$path)
  if (Test-Path "$path") {} else {
    mkdir "$path" | Out-Null
  }
  cd "$path"
}

# Create folders
write-host "Creating folders... (Installing to 'C:\users\$user_name\Documenta\Github\crosshell_zedix'"
GoFolder "C:\users\$user_name\Documenta\"
GoFolder "$(Get-Location)\Github\"
GoFolder "$(Get-Location)\crosshell_zedix\"

# preclean
if (Test-path repo_clone) {
  write-host "Removing old download..."
  del repo_clone -force -confirm
}

# Install dependencies
write-host "Installing dependencies..."
$envPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (!(Get-Command pwsh -ErrorAction SilentlyContinue)) {
  winget install Microsoft.Powershell -e -h
}
if (!(Get-Command python3 -ErrorAction SilentlyContinue)) {
    winget install Python.Python -e -h
}
if (!(Get-Command pip3 -ErrorAction SilentlyContinue)) {
    python3 -m ensurepip
}
$packages = @("pyyaml", "tqdm", "requests", "prompt_toolkit", "pygments")
pip3 install $packages


# Download archive
if (Test-path repo_clone.zip) {} else {
  write-host "Downloading archive..."
  iwr "https://github.com/simonkalmiclaesson/crosshell_zedix/archive/refs/heads/main.zip" -o repo_clone.zip
}

# Expand archive
write-host "Extracting archive..."
Expand-Archive repo_clone.zip
cd repo_clone\crosshell_zedix-main
copy assets\ ..\..\
copy crosshell.py ..\..\
cd ..\..

# Cleanup
if (Test-path repo_clone) {
  write-host "Cleaning up..."
  del repo_clone -force -confirm:$false -Recurse
}


# Create path file
write-host "proceeding to add to path..."
$pathtoadd = "$(Get-Location)\.path"
if (Test-Path "$pathtoadd\crosshell.bat") { '@python3 %~dp0\..\crosshell.py %*' | out-file "$pathtoadd\crosshell.bat" }
if (Test-Path "$pathtoadd\crsh.bat") { '@python3 %~dp0\..\crosshell.py %*' | out-file "$pathtoadd\crsh.bat" }

# add to path
if (test-path .path) {} else {
  mkdir .path | Out-Null
}
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$pathtoadd*") {
  $newPath = "$userPath;$pathtoadd"
  [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
}

# Ensure execution policy
Write-Host "Running powershell scripts in crosshell needs ExecutionPolicy to be changed, this allowes any powershell script to be run on the system and may leed to security problems. Do you agree to change it? (Write 'n' to not, however then you can't run powershell scripts in crosshell) [y/n]" -ForegroundColor Red -NoNewline
$c = Read-Host
if ($c.ToLower() -eq "y") {
  Start-Process powershell.exe -Verb RunAs -ArgumentList "-Command Set-ExecutionPolicy Bypass -Scope CurrentUser"
  Start-Process pwsh.exe -Verb RunAs -ArgumentList "-Command Set-ExecutionPolicy Bypass -Scope CurrentUser"
}

# End
$host.ui.rawui.windowtitle = $old_windowtitle
Set-Location $old_dir