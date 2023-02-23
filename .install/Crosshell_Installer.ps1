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
GoFolder "C:\users\$user_name\Documenta\"
GoFolder "$(Get-Location)\Github\"
GoFolder "$(Get-Location)\crosshell_zedix\"

# Download archive
if (Test-path repo_clone.zip) {} else {
  iwr "https://github.com/simonkalmiclaesson/crosshell_zedix/archive/refs/heads/main.zip" -o repo_clone.zip
}
Expand-Archive repo_clone.zip

# End
$host.ui.rawui.windowtitle = $old_windowtitle
Set-Location $old_dir