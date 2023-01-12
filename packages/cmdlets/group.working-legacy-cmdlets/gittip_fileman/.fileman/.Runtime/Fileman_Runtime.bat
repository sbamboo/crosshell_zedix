<# : Start of runtime block

REM Shell things
@echo off & setlocal
set "POWERSHELL_BAT_ARGS=%*"
REM Install Pwsh and start it
powershell $old_ErrorActionPreference = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'; $title = $host.ui.rawui.windowtitle; $host.ui.rawui.windowtitle = 'Pwsh runtime V.3.1 [win_batch]'; $env:path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); if(Get-Command 'pwsh') {} else { $curdir = $pwd; cd $env:temp; if (test-path 'pwsh_runtime_install') {} else {mkdir 'pwsh_runtime_install'}; cd 'pwsh_runtime_install'; $tempLoc = $pwd; cd $curdir; Invoke-RestMethod 'https://aka.ms/install-powershell.ps1' -outfile $tempLoc/inst.ps1; set-executionpolicy bypass -force; . $tempLoc/inst.ps1 -AddToPath; rmdir $tempLoc -recurse -force; write-host '[Runtime]: Installed!' -f green}; $ErrorActionPreference = $old_ErrorActionPreference; $env:path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); $host.ui.rawui.windowtitle = $title; cls; pwsh -noprofile -NoLogo -Command 'iex (${%~f0} ^| out-string)'
REM Exit prompt
exit /b %errorlevel%

: End of runtime block #>


cd ..
.\Fileman.ps1