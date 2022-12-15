#Additional functions for fileman, needed for functionality.
#falls under the included license file

#Set CurPath
function s-cp {
    $script:curpath = $pwd
}

#Go Curpath
function g-cp {
    cd $script:curpath
}

#bufferScript by Simon Kalmi Claesson for crosshell, used here for buffer save functionality
function buffer {
  param([switch]$save,[switch]$load)
  if ($save) {
    $w = $host.ui.rawui.buffersize.width
    $h = $host.ui.rawui.buffersize.height
    $Source = New-Object System.Management.Automation.Host.Rectangle 0, 0, $w, $h
    $script:fman_ScreenBuffer = $host.UI.RawUI.GetBufferContents($Source)
  } elseif ($load) {
    $w = $host.ui.rawui.buffersize.width
    $h = $host.ui.rawui.buffersize.height
    $Source = New-Object System.Management.Automation.Host.Rectangle 0, 0, $w, $h
    $host.UI.RawUI.SetBufferContents((New-Object System.Management.Automation.Host.Coordinates $Source.Left, $Source.Top), $script:fman_ScreenBuffer)
    $c = 'echo "`e[' + ($h-4) + 'B"'
    iex($c)
  }
}


#Contains
function Contains($i,$c,$o) {
  $orgI = $i
  #Any
  if ($o -like "*any*") {
    $i = $i -replace "$c",""
  }
  #Start
  if ($o -like "*start*") {
    $i = $i.TrimStart("$c")
  }
  #End
  if ($o -like "*end*") {
    $i = $i.TrimEnd("$c")
  }
  #Check Result
  if ($i -eq $orgI) {
    return $false
  } else {
    return $true
  }
}

#GetInput
function GetInput($que,$fore,$back) {
  write-host -nonewline "$que" -f $fore -b $back
  $in = Read-host
  return $in
}

#FormatConfig
function FormatConfig($varName) {
  #Start StringBuild
  $string = "$varName "
  #Get Type
  $type = '$' + "$varName" + '.GetType().name'
  $type = iex($type)
  #Get Type2
  $type2 = '$' + "$varName" + '.GetType().BaseType.name'
  $type2 = iex($type2)
  #StringBuild if string
  if ($type -eq "String") {
    $string += iex('$' + "$varName")
  }
  #StringBuild if array
  if ($type2 -eq "Array") {
    $tmp0 = '$' + "$varName" + '[0]'
    $tmp1 = '$' + "$varName" + '[1]'
    $tmp0 = iex($tmp0)
    $tmp1 = iex($tmp1)
    if ($tmp0 -ne "") {
      $string += "$tmp0 "
    }
    if ($tmp1 -ne "") {
      $string += "$tmp1"
    }
  }
  return $string
}

#SaveOrg
function SaveOrg($varName) {
  s-cp
  cd $corepath
  $command = "FormatConfig $varName"
  iex($command) | Out-File -file "$org_file" -append
  g-cp
}

#SaveNew
function SaveNew($varName) {
  s-cp
  cd $corepath
  $command = "FormatConfig $varName"
  iex($command) | Out-File -file "$new_file" -append
  g-cp
}

#SaveOrgConfig
function SaveOrgConfig {
  $script:org_pref = $pref
  $script:org_setpref = $setpref
  $script:org_fm_editor = $fm_editor
  $script:org_fm_mode_shash = $fm_mode_shash
  $script:org_fm_mode_simple = $fm_mode_simple
  $script:org_fm_mode_diagram = $fm_mode_diagram
  $script:org_fm_autoLoadSettings = $fm_autoLoadSettings
  $script:org_fm_savelastDir = $fm_savelastDir
  $script:org_fm_loadlastDir = $fm_loadlastDir

  [array]$script:org_theme_folder = $theme_folder
  [array]$script:org_theme_item = $theme_item
  [array]$script:org_theme_LWtime = $theme_LWtime
  [array]$script:org_theme_size = $theme_size
  [array]$script:org_theme_zip = $theme_zip
  [array]$script:org_theme_text = $theme_text
  [array]$script:org_theme_console = $theme_console
  [array]$script:org_theme_diagram = $theme_diagram
  [array]$script:org_theme_dirNote = $theme_dirNote
  [array]$script:org_theme_hash = $theme_hash

  #WriteToFile
  if (Test-Path $org_file) {del $org_file}
  SaveOrg pref
  SaveOrg setpref
  SaveOrg fm_editor
  SaveOrg fm_mode_shash
  SaveOrg fm_mode_simple
  SaveOrg fm_mode_diagram
  SaveOrg fm_autoLoadSettings
  SaveOrg fm_savelastDir
  SaveOrg fm_loadlastDir
  SaveOrg theme_folder
  SaveOrg theme_item
  SaveOrg theme_LWtime
  SaveOrg theme_size
  SaveOrg theme_zip
  SaveOrg theme_text
  SaveOrg theme_console
  SaveOrg theme_diagram
  SaveOrg theme_dirNote
  SaveOrg theme_hash
}

#Save Config
function SaveConfig {
  #WriteToFile
  if (Test-Path $new_file) {del $new_file -force}
  SaveNew pref
  SaveNew setpref
  SaveNew fm_editor
  SaveNew fm_mode_shash
  SaveNew fm_mode_simple
  SaveNew fm_mode_diagram
  SaveNew fm_autoLoadSettings
  SaveNew fm_savelastDir
  SaveNew fm_loadlastDir
  SaveNew theme_folder
  SaveNew theme_item
  SaveNew theme_LWtime
  SaveNew theme_size
  SaveNew theme_zip
  SaveNew theme_text
  SaveNew theme_console
  SaveNew theme_diagram
  SaveNew theme_dirNote
  SaveNew theme_hash
}
#Load Config
function LoadConfig($file) {
  s-cp
  cd $corepath
  $config = gc $file
  foreach ($_ in $config) {
    $line = $_
    [array]$configL = $line -split " "
    if (($configL.length -1) -eq "1") {
      $command = 'Set-Variable -name ' + $configL[0] + ' -scope Script -value "' + $configL[1] + '"'
    } else {
      $command = 'Set-Variable -name ' + $configL[0] + ' -scope Script -value "' + $configL[1] + '","' + $configL[2] + '"'
    }
    iex($command)
  }
  g-cp
}


#ConvertBytes
#Orignal from: https://learn-powershell.net/2010/08/29/convert-bytes-to-highest-available-unit/
function Convert-BytesToSize {
    [CmdletBinding()]
    Param(
      [parameter(Mandatory=$False,Position=0)][int64]$Size
    )
    Switch ($Size) {
        {$Size -gt 1000000000PB} {
            $text = "$([math]::Round(($Size / 1000000000PB)))YB"
            Break
        }
        {$Size -gt 1000000PB} {
            $text = "$([math]::Round(($Size / 1000000PB)))ZB"
            Break
        }
        {$Size -gt 1000PB} {
            $text = "$([math]::Round(($Size / 1000PB)))EB"
            Break
        }
        {$Size -gt 1PB} {
            $text = "$([math]::Round(($Size / 1PB)))PB"
            Break
        }
        {$Size -gt 1TB} {
            $text = "$([math]::Round(($Size / 1TB)))TB"
            Break
        }
        {$Size -gt 1GB} {
            $text = "$([math]::Round(($Size / 1GB)))GB"
            Break }
        {$Size -gt 1MB} {
            $text = "$([math]::Round(($Size / 1MB)))MB"
            Break
        }
        {$Size -gt 1KB} {
            $text = "$([math]::Round(($Size / 1KB)))KB"
            Break
        }
        Default {
            $text = "$([math]::Round($Size,2))B "
            Break
        }
    }
    Return $text
}

#FormatSize
function FormatSize($num) {
  [string]$size = Convert-BytesToSize $num
  if (($size.length-2) -eq "1") {
    $size = "$size" + "  "
  }
  if (($size.length-2) -eq "2") {
    $size = "$size" + " "
  }
  return $size
}

#CheckConfig
function CheckConfig {
  s-cp
  cd $corepath
  if (Test-Path $new_file) {
    $config = gc $new_file
    foreach ($_ in $config) {
      if ($_ -eq "fm_autoLoadSettings true") {
        $script:fm_autoLoadSettings = "$True"
      }
    }
  }
  g-cp
}


#write-menu item
function Write-MenuItem($Mode,$text,$r,$Ifc,$Dfc,$prefix) {
  [string]$result = $result
  #SingleMode
  if ($mode -eq "Singl") {
    $r = iex($r)
    $text = $text -replace "§","$r"
    write-host "$text"
  }
  #MultiMode
  elseif ($mode -eq "Multi") {
    [array]$textA = $text -split "§"
    $r = iex($r)
    $f = $r[0]
    $b = $r[1]
    write-host -nonewline $textA[0] -f $theme_text[0] -b $theme_text[1]
    write-host -nonewline $r -f $f -b $b
    write-host ")" -f $theme_text[0] -b $theme_text[1]
  }
  #FormatedMenu
  elseif ($mode -eq "Fmenu") {
    [string]$obj = $text
    [string]$desc = $r
    write-host -nonewline " " -f $theme_text[0] -b $theme_text[1]
    write-host -nonewline "$prefix$obj" -f $Ifc -b $theme_text[1]
    write-host -nonewline " :  " -f $theme_text[0] -b $theme_text[1]
    write-host "$desc" -f $Dfc -b $theme_text[1]
  }
  #General
  else {
    write-host "$text" -f $theme_text[0] -b $theme_text[1]
  }
}

#ReloadConsoleTheme
function ReloadConsoleTheme {
  $host.ui.rawui.foregroundcolor = $theme_console[0]
  $host.ui.rawui.backgroundcolor = $theme_console[1]
}


#LastDIr
function LastDir($action, $path) {
  s-cp
  cd $corepath
  if ($action -like "*save*") {
    [string]$ld_dir = $path
    write-host "$ld_dir";pause
    if (Test-Path $lwd_file) {del $lwd_file}
    $ld_dir | Out-file -file $lwd_file -append
  }
  if ($action -like "*load*") {
    if (Test-Path $lwd_file) {
      $ld_dir = gc $lwd_file
      return "$ld_dir"
    } else {
      return $fm_startpath
    }
  }
  g-cp
}


#Set-Callback
function fm_Set-Callback($text,$f,$b) {
  $foreground = $def_forecolor
  $background = $def_backcolor
  if ($f) {$foreground = $f}
  if ($b) {$background = $b}
  $script:fm_callback_command = 'write-host "' + "$text" + '" -f ' + "$foreground -b $background"
}
#Reset-Callback
function fm_Reset-Callback {
  $script:fm_callback_command = ""
}
#Run-Callback
function fm_Run-Callback {
  if ($script:fm_callback_command -ne "") {
    iex($fm_callback_command)
    fm_Reset-Callback
  }
}

#ColorValid
function Is-ColorValid($color) {
  [array]$validColors = [Enum]::GetValues([System.ConsoleColor])
  if ($validColors -like "$color") {return $true} else {return $false}
}

#ColorInputValidator
function ColorInputValidator($colors,$fallback) {
  [array]$test = $colors -split " "
  $col1 = $test[0]
  $col2 = $test[1]
  $valid = $false
  if (Is-ColorValid "$col1" -eq "true") {
    if (Is-ColorValid "$col2" -eq "true") {
      $valid = $true
    } else {
      $valid = $false
    }
  } else {
    $valid = $false
  }
  if ($valid -eq $true) {
    [array]$color_ARR = "$col1","$col2"
    return $color_ARR
  } else {
    [string]$fm_callback_MSG = "'" + "$test" + "'" + " is not a valid color option"
    fm_Set-Callback "$fm_callback_MSG" "red"
    [array]$f = $fallback -split " "
    $f1 = $f[0]
    $f2 = $f[1]
    [array]$fallb = "$f1","$f2"
    return $fallb
  }
}

#ShowBar
function Showbar {
  $bar = "-" * ((Get-Host).ui.rawui.buffersize.width - 1)
  write-host $bar -f $theme_text[0] -b $theme_text[1]
}

#ShowDiagram
function ShowDiagram {
  $f = "Green"
  $b = $def_backcolor
  if ($theme_diagram) {
    $f = $theme_diagram[0]
    $b = $theme_diagram[1]
  }
  write-host "Size    LastWrite-Time        Name" -f $f -b $b
  write-host "----    -------------------   ----" -f $f -b $b
}
