#Fileman pwsh-core version
#Fileman is made by Simon Kalmi Claesson
#License information in "license"
#

#params
Param(
    #in param
    [Parameter(ValueFromPipeline=$true)]
    [Alias("n")]
    [Alias("in")]
    [string]$inp,
    
    #base params
    [Alias("p")]
    [string]$path,
    [Alias("m")]
    [string]$mode,

    #cli usage params
    [Alias("re")]
    [switch]$remove,
    [Alias("cp")]
    [switch]$copy,
    [Alias("mi")]
    [switch]$makeitem,
    [Alias("md")]
    [switch]$makeDir,
    [Alias("st")]
    [switch]$startItem,
    [Alias("ed")]
    [switch]$editItem,
    [Alias("rn")]
    [switch]$rename,
    [Alias("zi")]
    [Alias("compress")]
    [switch]$zip,
    [Alias("uz")]
    [Alias("extract")]
    [switch]$unzip,
    [Alias("xp")]
    [switch]$explorer,

    [Alias("opt")]
    [switch]$options,
    [Alias("hlp")]
    [switch]$help,
    [Alias("lice")]
    [switch]$license,
    [Alias("i")]
    [Alias("inf")]
    [switch]$info,

    [string]$cliPassedPath

)

#cliPassedPath
if ($cliPassedPath) {
  cd $cliPassedPath
}

#BuiltIn Settings
  #Default Settings
  $pref = "-"
  $setpref = "/"
  $fm_editor = "Notepad.exe"
  $fm_mode_shash = "false"
  $fm_mode_simple = "false"
  $fm_mode_diagram = "false"
  $fm_autoLoadSettings = "false"
  $fm_savelastDir = "false"
  $fm_loadlastDir = "false"

  #Default theme
  $def_forecolor = $host.ui.rawui.foregroundcolor
  $def_backcolor = $host.ui.rawui.backgroundcolor
  [array]$theme_folder = "$def_forecolor","$def_backcolor"
  [array]$theme_item = "$def_forecolor","$def_backcolor"
  [array]$theme_LWtime = "$def_forecolor","$def_backcolor"
  [array]$theme_size = "$def_forecolor","$def_backcolor"
  [array]$theme_zip = "$def_forecolor","$def_backcolor"
  [array]$theme_text = "$def_forecolor","$def_backcolor"
  [array]$theme_console = "$def_forecolor","$def_backcolor"
  [array]$theme_diagram = "$def_forecolor","$def_backcolor"
  [array]$theme_dirNote = "$def_forecolor","$def_backcolor"
  [array]$theme_hash = "$def_forecolor","$def_backcolor"

  #Files
  $org_file = "orginal.Rcfg"
  $new_file = "options.Rcfg"
  $lwd_file = "LastWorkDir.Mem"




#Internal
$fm_author = "Simon Kalmi Claesson"
$fm_version = "3.0_beta6"
$fm_description = "Fileman is a simple file manager written in Powershell"

#HandleParam

#buffer -save

#base
if ($mode -eq "simple") {$mode = "$true"} else {$mode = "$false"}
#cliusage
[string]$cli_cmdpass = ""
if ($remove) {[string]$cli_cmdpass = "$pref" + "re"}
if ($copy) {[string]$cli_cmdpass = "$pref" + "cp"}
if ($makeItem) {[string]$cli_cmdpass = "$pref" + "mi"}
if ($makeDir) {[string]$cli_cmdpass = "$pref" + "md"}
if ($startItem) {[string]$cli_cmdpass = "$pref" + "st"}
if ($editItem) {[string]$cli_cmdpass = "$pref" + "ed"}
if ($rename) {[string]$cli_cmdpass = "$pref" + "rn"}
if ($zip) {[string]$cli_cmdpass = "$pref" + "zi"}
if ($unzip) {[string]$cli_cmdpass = "$pref" + "uz"}
if ($explorer) {[string]$cli_cmdpass = "$pref" + "xp"}

if ($options) {[string]$cli_cmdpass = "$setpref" + "opt"}
if ($info) {[string]$cli_cmdpass = "$setpref" + "info"}
if ($help) {[string]$cli_cmdpass = "$setpref" + "help"}
if ($license) {[string]$cli_cmdpass = "$setpref" + "lice"}
if ($inp) {$cli_cmdpass += " $inp"}
if ($cli_cmdpass -ne "") {$climode = $true} else {$climode = $false}


#Load additions
$corePath = $PSScriptRoot
$cp = Get-location
cd $corePath
. ./addins.ps1
cd $cp

#StartingDir
  $script:fm_startpath = $Pwd
  cd $fm_startpath

#Settings
SaveOrgConfig
#LoadConfig
LoadConfig "$org_file"
#CheckConfig
CheckConfig
if ($fm_autoLoadSettings -eq "$true") {
  LoadConfig "$new_file"
}
#DirHandle
if ($fm_loadlastDir -eq "true") {$tmp = LastDir load; cd $tmp}
if ($path) {cd $path}
#ModeParam
if ($mode) {$fm_mode_simple = "$mode"} else {$fm_mode_simple = "$false"}

#DefineCallBack
fm_Reset-Callback

#MainLoop
$MainLoop = $true
while ($MainLoop -eq "$true") {
    #pre item view
      #LoadConsoleTheme
      ReloadConsoleTheme
      #saveDir
      $fm_state_lastdir = $pwd
    if (!$cli_cmdpass) {cls}
    $cfgCmd = "$setpref" + "opt"
    $hlpCmd = "$setpref" + "help"
    $infCmd = "$setpref" + "info"
    $licCmd = "$setpref" + "lice"
    #WindowTitle
    $host.ui.rawui.windowtitle = "Fileman $fm_version"
    #TitleBar
    if ($cli_cmdpass) {} else {
      $headstr = 'Write "' + "$cfgCmd" + '" for settings, "' + "$hlpCmd" + '" for help or "' + "$infCmd" + '" for for info.'
      write-host "$headstr" -f $theme_text[0]-b $theme_text[1]
      Showbar
      if ($fm_mode_simple -eq "$false") {
        write-host -nonewline "CurrentDir: " -f $theme_text[0] -b $theme_text[1]
        write-host "$pwd`n" -f green -b $theme_text[1]
      }
    }
    #DiagramMode
    if ($fm_mode_diagram -eq "true") {ShowDiagram}
    #get files and folders
    $items = Get-ChildItem

    #Show Folders
    if ($climode -eq $false) {
      if ($fm_mode_simple -eq "$true") {
          #Simple Mode
          foreach ($item in $items) {
            write-host $item.name -f $theme_text[0]-b $theme_text[1]
          }
      } else {
          #Advanced Mode
          foreach ($item in $items) {
              #GetInfo
              $Fullname = $item.name
              $name = $Fullname.Split("."); $name = $name[0..($name.length-2)]
              $extension = $Fullname.Split("."); $extension = $extension[$extension.length-1]
              if ($item.mode -notlike "*d*") {$hash = $(Get-FileHash $item.name).Hash} else {$hash = "                                                                "}
              #Folder
              if ($item.mode -like "*d*") {
                  write-host -nonewline '<Dir>' -f $theme_dirNote[0] -b $theme_dirNote[1]
                  write-host -nonewline "   "
                  if ($fm_mode_shash -eq $true) {
                    write-host -nonewline "$hash" -f $theme_hash[0] -b $theme_hash[1]
                    write-host -nonewline "   "
                  }
                  write-host -nonewline $item.LastWriteTime -f $theme_LWtime[0] -b $theme_LWtime[1]
                  write-host -nonewline "   "
                  write-host $item.name -f $theme_folder[0] -b $theme_folder[1]

              } elseif ($extension -like "*zip*") {
                #Zip archive
                  $size = FormatSize $item.length
                  write-host -nonewline $size -f $theme_size[0] -b $theme_size[1]
                  write-host -nonewline "   "
                  if ($fm_mode_shash -eq $true) {
                    write-host -nonewline "$hash" -f $theme_hash[0] -b $theme_hash[1]
                    write-host -nonewline "   "
                  }
                  write-host -nonewline $item.LastWriteTime -f $theme_LWtime[0] -b $theme_LWtime[1]
                  write-host -nonewline "   "
                  write-host $item.name -f $theme_zip[0] -b $theme_zip[1]

              } else {
                #Item
                  $size = FormatSize $item.length
                  write-host -nonewline $size -f $theme_size[0] -b $theme_size[1]
                  write-host -nonewline "   "
                  if ($fm_mode_shash -eq $true) {
                    write-host -nonewline "$hash" -f $theme_hash[0] -b $theme_hash[1]
                    write-host -nonewline "   "
                  }
                  write-host -nonewline $item.LastWriteTime -f $theme_LWtime[0] -b $theme_LWtime[1]
                  write-host -nonewline "   "
                  write-host $item.name -f $theme_item[0] -b $theme_item[1]
              }
          }
      }
      #HandleInput
        write-host -nonewline "[cd/op]: " -f $theme_text[0] -b $theme_text[1]
        fm_Run-Callback
        $inu = read-host
        $in = "$inu"
    } else {
      $in = $cli_cmdpass
    }
    #Special Cases
      #Username
      if ("$in" -like "*~usr*") {
        $in = $in -replace "~usr","$env:username"
      }
      #cd
      if ("$in" -like "cd*") {
        $in = $in -replace "cd ",""
        $in = $in -replace "cd",""
      }
    #HandleOperations
      #remove
      $check = "$pref" + "re"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        del $in
      }
      #copy
      $check = "$pref" + "cp"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        [array]$inA = $in -split " "
        $file = $inA[0]
        $location =$inA[1]
        copy $file $location
      }
      #makeItem
      $check = "$pref" + "mi"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        write-host "" | Out-File -file $in
      }
      #makeDirectory
      $check = "$pref" + "md"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        New-Item -path "$pwd/$in" -ItemType Directory
      }
      #startItem
      $check = "$pref" + "st"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        start "$in"
      }
      #editItem
      $check = "$pref" + "ed"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        start $fm_editor "$in"
      }
      #rename
      $check = "$pref" + "rn"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        [array]$inA = $in -split " "
        $old = $inA[0]
        $new =$inA[1]
        ren $old $new
      }
      #Zip
      $check = "$pref" + "zi"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        [array]$inA = $in -split " "
        $file = $inA[0]
        $location =$inA[1]
        if ($location) {
          Compress-Archive -path "$pwd/$file" -destinationpath "$location"
        } else {
          Compress-Archive -path "$pwd/$file" -destinationpath "$pwd"
        }
      }
      #unzip
      $check = "$pref" + "uz"
      if ("$in" -like "$check*") {
        $in = $in -replace "$check ",""
        [array]$inA = $in -split " "
        $file = $inA[0]
        $location =$inA[1]
        if ($location) {
          Expand-Archive -path "$pwd/$file" -destinationpath "$location"
        } else {
          Expand-Archive -path "$pwd/$file" -destinationpath "$pwd"
        }
      }
      #exit
      $check = "$pref" + "ex"
      if ("$in" -like "$check*") {
        $MainLoop = $false
      } 
      #explorer
      $check = "$pref" + "xp"
      if ("$in" -like "$check*") {
        if ($isWindows) {
          $in = $in -replace "$check ",""
          explorer "$in"
        }
      } 
      #Settings
      $check = "$setpref" + "opt"
      if ("$in" -like "$check*") {
        $in = "$in" -replace "$check",""
        $in = $in.TrimStart(" ")
        #Settings UI
        $keepSettings = "$true"
        while ($keepSettings -eq "$true") {
          cls
          Write-host "Fileman Settings:" -f $theme_text[0] -b $theme_text[1]
          ShowBar
          write-MenuItem singl "  [1]  :  Prefix (§)" '$pref'
          write-MenuItem singl "  [2]  :  SetPrefix (§)" '$setpref'
          write-MenuItem singl "  [3]  :  Editor (§)" '$fm_editor'
          write-MenuItem -text "                                      "
          write-MenuItem multi "  [4]  :  Text Theme (§)" '$theme_text'
          write-MenuItem multi "  [5]  :  Item Theme (§)" '$theme_item'
          write-MenuItem multi "  [6]  :  Folder Theme (§)" '$theme_folder'
          write-MenuItem multi "  [7]  :  Size Theme (§)" '$theme_size'
          write-MenuItem multi "  [8]  :  LWtime Theme (§)" '$theme_LWtime'
          write-MenuItem multi "  [9]  :  Zip Theme (§)" '$theme_zip'
          write-MenuItem multi "  [0]  :  Console Theme (§)" '$theme_console'
          write-MenuItem multi "  [G]  :  Diagram Theme (§)" '$theme_diagram'
          write-MenuItem multi "  [H]  :  Dir-Note Theme (§)" '$theme_dirNote'
          write-MenuItem multi "  [J]  :  Hash Theme (§)" '$theme_hash'
          write-MenuItem -text "                                      "
          write-MenuItem singl "  [I]  :  Show Hashes (§)" '$fm_mode_shash' 
          write-MenuItem singl "  [A]  :  SimpleMode (§)" '$fm_mode_simple'
          write-MenuItem singl "  [B]  :  DiagramMode (§)" '$fm_mode_diagram'
          write-MenuItem -text "                                      "
          write-MenuItem singl "  [C]  :  AutoLoad Settings (§)" '$fm_autoloadsettings'
          write-MenuItem singl "  [D]  :  AutoSave LastWorkingDir (§)" '$fm_savelastDir'
          write-MenuItem singl "  [F]  :  AutoLoad LastWorkingDir (§)" '$fm_loadlastDir'
          write-MenuItem -text "                                      "
          write-MenuItem -text "  [S]  :  Save Settings"
          write-MenuItem -text "  [L]  :  Load Settings"
          write-MenuItem -text "  [R]  :  Reset Settings"
          write-MenuItem -text "                                      "
          write-MenuItem -text "  [E]  :  Continue/Escape"
          ShowBar
          write-host -nonewline "Setting: " -f $theme_text[0] -b $theme_text[1]
          fm_Run-Callback
          $setIn = Read-Host
          #Handle Settings
            #AutoLoadSettings
            if ("$setIN" -like "C*") {
              $in2 = GetInput "AutoLoad Settings: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                if ("$in2" -eq "$true") {
                  $fm_autoLoadSettings = "$true"
                }
                if ("$in2" -eq "$false") {
                  $fm_autoLoadSettings = "$false"
                }
              }
            }
            #SaveLastDir
            if ("$setIN" -like "D*") {
              $in2 = GetInput "Save LastWorkingDir: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                if ("$in2" -eq "$true") {
                  $fm_savelastDir = "$true"
                }
                if ("$in2" -eq "$false") {
                  $fm_savelastDir = "$false"
                }
              }
            }
            #LoadLastDir
            if ("$setIN" -like "F*") {
              $in2 = GetInput "Load LastWorkingDir: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                if ("$in2" -eq "$true") {
                  $fm_loadlastDir = "$true"
                }
                if ("$in2" -eq "$false") {
                  $fm_loadlastDir = "$false"
                }
              }
            }
            #Show Hashes
            if ("$setIN" -like "I*") {
              $in2 = GetInput "Show Hashes: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                $fm_mode_shash = $in2
              } else {
                $fm_mode_shash = $org_fm_mode_shash
              }
            }
            #SimpleMode
            if ("$setIN" -like "A*") {
              $in2 = GetInput "SimpleMode: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                $fm_mode_simple = $in2
              } else {
                $fm_mode_simple = $org_fm_mode_simple
              }
            }
            #DiagramMode
            if ("$setIN" -like "B*") {
              $in2 = GetInput "DiagramMode: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                $fm_mode_diagram = $in2
              } else {
                $fm_mode_diagram = $org_fm_mode_diagram
              }
            }
            #Prefix
            if ("$setIN" -like "1*") {
              $in2 = GetInput "Prefix: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                if ("$in2" -eq '""') {$in2 = $in2 -replace '""',''}
                $pref = $in2
              } else {
                $pref = $org_pref
              }
            }
            #SetPrefix
            if ("$setIN" -like "2*") {
              $in2 = GetInput "SetPrefix: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                if ("$in2" -eq '""') {$in2 = $in2 -replace '""',''}
                $setpref = $in2
              } else {
                $setpref = $org_setpref
              }
            }
            #Editor
            if ("$setIN" -like "3*") {
              $in2 = GetInput "Editor: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                $fm_editor = $in2
              } else {
                $fm_editor = $org_fm_editor
              }
            }
            #TextTheme
            if ("$setIN" -like "4*") {
              $in2 = GetInput "Text Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_text = ColorInputValidator "$in2" "$org_theme_text"
              } else {
                [array]$theme_text = $org_theme_text
              }
            }
            #ItemTheme
            if ("$setIN" -like "5*") {
              $in2 = GetInput "Item Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_item = ColorInputValidator "$in2" "$org_theme_item"
              } else {
                [array]$theme_item = $org_theme_item
              }
            }
            #FolderTheme
            if ("$setIN" -like "6*") {
              $in2 = GetInput "Folder Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_folder = ColorInputValidator "$in2" "$org_theme_folder"
              } else {
                [array]$theme_folder = $org_theme_folder
              }
            }
            #SizeTheme
            if ("$setIN" -like "7*") {
              $in2 = GetInput "Size Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_size = ColorInputValidator "$in2" "$org_theme_size"
              } else {
                [array]$theme_size = $org_theme_size
              }
            }
            #LWtimeTheme
            if ("$setIN" -like "8*") {
              $in2 = GetInput "LWtime Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_LWtime = ColorInputValidator "$in2" "$org_theme_LWtime"
              } else {
                [array]$theme_LWtime = $org_theme_LWtime
              }
            }
            #ZipTheme
            if ("$setIN" -like "9*") {
              $in2 = GetInput "Zip Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_zip = ColorInputValidator "$in2" "$org_theme_zip"
              } else {
                [array]$theme_zip = $org_theme_zip
              }
            }
            #ConsoleTheme
            if ("$setIN" -like "0*") {
              $in2 = GetInput "Console Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_console = ColorInputValidator "$in2" "$org_theme_console"
              } else {
                [array]$theme_console = $org_theme_console
              }
            }
            #ConsoleTheme
            if ("$setIN" -like "G*") {
              $in2 = GetInput "Diagram Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_diagram = ColorInputValidator "$in2" "$org_theme_diagram"
              } else {
                [array]$theme_diagram = $org_theme_diagram
              }
            }
            #DirNoteTheme
            if ("$setIN" -like "H*") {
              $in2 = GetInput "Diagram Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_dirNote = ColorInputValidator "$in2" "$org_theme_dirNote"
              } else {
                [array]$theme_dirNote = $org_theme_dirNote
              }
            }
            #HashTheme
            if ("$setIN" -like "J*") {
              $in2 = GetInput "Hash Theme: " $theme_text[0] $theme_text[1]
              if ($in2 -ne "") {
                [array]$theme_hash = ColorInputValidator "$in2" "$org_theme_hash"
              } else {
                [array]$theme_hash = $org_theme_hash
              }
            }
            #Esc
            if ("$setIN" -like "e*") {
              $keepSettings = "$false"
              if ($climode) {exit}
            }
            #SaveSettings
            if ("$setIN" -like "s*") {
              SaveConfig
            }
            #LoadSettings
            if ("$setIN" -like "l*") {
              $curP2 = get-location
              cd $corepath
              if (Test-Path $new_file) {
                LoadConfig "$new_file"
              } else {
                LoadConfig "$org_file"
              }
              cd $curP2
            }
            #ResetSettings
            if ("$setIN" -like "R*") {
              LoadConfig "$org_file"
            }
            #Empty
            if ("$setIn" -eq "") {
              $keepSettings = "$false"
            }
        }
      }
      #Help
      $check = "$setpref" + "help"
      if ("$in" -like "$check*") {
        #HelpUI
        cls
        Write-MenuItem -text "Fileman Help:"
        ShowBar
        write-MenuItem Fmenu "re  " "Removes a file/folder" green blue "$pref"
        write-MenuItem Fmenu "cp  " "Copies file/folder" green blue "$pref"
        write-MenuItem Fmenu "mi  " "Creates new file" green blue "$pref"
        write-MenuItem Fmenu "md  " "Creates new folder" green blue "$pref"
        write-MenuItem Fmenu "st  " "Starts a file" green blue "$pref"
        write-MenuItem Fmenu "ed  " "Opens a file in default editor ($fm_editor)" green blue "$pref"
        write-MenuItem Fmenu "rn  " "Renames a file/folder" green blue "$pref"
        write-MenuItem Fmenu "zi  " "Creates a zip archive of file/folder" green blue "$pref"
        write-MenuItem Fmenu "uz  " "Unzips a zip archive" green blue "$pref"
        write-MenuItem Fmenu "ex  " "Exits fileman" green blue "$pref"
        if ($isWindows) {write-MenuItem Fmenu "xp  " "Opens the file/folder in explorer.exe (win-only)" green blue "$pref"}
        write-MenuItem -text "                                      "
        write-MenuItem Fmenu "opt " "Opens Settings" green blue "$setpref"
        write-MenuItem Fmenu "info" "Shows info about fileman" green blue "$setpref"
        write-MenuItem Fmenu "help" "Shows this menu/help-menu" green blue "$setpref"
        write-MenuItem Fmenu "lice" "Shows the fileman license" green blue "$setpref"
        ShowBar
        if ($climode) {exit} else {pause}
      }
      #License
      $check = "$setpref" + "lice"
      if ("$in" -like "$check*") {
        #HelpUI
        cls
        Write-MenuItem -text "Fileman License:"
        ShowBar
        $licensefile = "$PSScriptRoot\LICENSE"
        if (Test-Path $licensefile) {
          $licensefile_data = Get-Content $licensefile -raw
          write-host $licensefile_data -f darkgreen
        } else {
          Write-host -nonewline "No license file could be found, please check your install. " -f red
          Write-host "(The license can be found at the place you downloaded fileman)" -f darkred
        }
        ShowBar
        if ($climode) {exit} else {pause}
      }
      #Info
      $check = "$setpref" + "info"
      if ("$in" -like "$check*") {
        #InfoUI
        cls
        Write-MenuItem -text "Fileman Info:"
        ShowBar
        Write-MenuItem -text "$fm_description"
        Write-MenuItem -text "Made by: $fm_author"
        Write-MenuItem -text "Version: $fm_version"
        Write-MenuItem -text "                                      "
        Write-MenuItem -text "Fileman_binPath: $corepath"
        ShowBar
        if ($climode) {exit} else {pause}
      }
      #EndFix
      if ("$in" -like "$setpref*") {
      } else {
        #ChangeDir
        if ($mainLoop -eq "True") {
          if ($climode) {exit}
          if ($in) {
            if (Test-path "$in") {
              cd $in
              if ($fm_savelastDir -eq "True") {LastDir save "$pwd"}
            } else {
              [string]$fm_callback_MSG = "Directory '" + "$in" + "'" + " couldn't be found."
              fm_Set-Callback "$fm_callback_MSG" "red"
            }
          }
        }
     }
}
#Post exit commands
cls
if ($fm_savelastDir -eq "True") {LastDir save "$fm_state_lastdir"}
#buffer -load
cd $fm_startpath
