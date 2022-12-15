<#
  .SYNOPSIS
  Bat inspired file content viewer.
#>

param($file)

# Settings
[int]$filenameHeight = 1
[int]$numRowWidthSides = 3
[int]$dividerWidth = 1
[int]$offsetWidth = 0
[string]$horizontalLine = "─"
[string]$verticalLine = "│"
[string]$topDivider = "┬"
[string]$midDivider = "┼"
[string]$bottomDivider = "┴"
[int]$contentOffsetVertical = 0
[int]$contentOffsetHorizontal = 1 
[array]$linesColor = "DarkGray"
[array]$contentColor = "Gray"

if ($file) {
    if (test-path "$file") {
        # Get file contents
        $content = get-content "$file"

        # Get file assoc
        if ($IsWindows) {
            $ext = "$file" | split-path -Extension
            $allFileEndingAssociations = Get-ChildItem "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\"
            $exist = $false
            foreach ($o in $allFileEndingAssociations) {
                if ($($o | split-path -extension) -eq "$ext") {
                    $exist = $true
                }
            }
            if ($exist -eq "$true") {
                $fileAssocData = Get-ItemProperty "Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\$ext\OpenWithList\"
                if (!$fileAssocData.b) {
                    $fileAssoc = $fileAssocData.a
                } else {
                    $fileAssoc = $fileAssocData.b
                }
            }
        }
        # File type mapping
        $fileTypeMap = @{
            ".ps1" = "Powershell";
            ".py"  = "Python";
            ".exe" = "Executable";
            ".crcmd" = "'Crosshell script file'";
            ".txt" = "Textfile";
            ".png" = "Image file";
            ".jpg" = "Image file";
            ".jpeg" = "Image file";
            ".bat" = "Windows command file";
            ".mp3" = "Audio file";
            ".wav" = "Audio file";
            ".mp4" = "Video file"
        }
        $fileType = $fileTypeMap["$ext"]


        # Handle some stuff
        $contentLength = $content.length
        if ($linesColor[0] -eq "§") {
            $linesColor = "$($host.UI.RawUI.ForegroundColor)","$($linesColor[1])"
        } elseif ($linesColor[1] -eq "§") {
            $linesColor = "$($linesColor[0])","$($host.UI.RawUI.BackgroundColor)"
        } elseif ($linesColor.length -eq 1) {
            $linesColor = "$($linesColor[0])","$($host.UI.RawUI.BackgroundColor)"
        } else {
            $linesColor = "$($host.UI.RawUI.ForegroundColor)","$($host.UI.RawUI.BackgroundColor)"
        }
        if ($contentColor[0] -eq "§") {
            $contentColor = "$($host.UI.RawUI.ForegroundColor)","$($contentColor[1])"
        } elseif ($contentColor[1] -eq "§") {
            $contentColor = "$($contentColor[0])","$($host.UI.RawUI.BackgroundColor)"
        } elseif ($contentColor.length -eq 1) {
            $contentColor = "$($contentColor[0])","$($host.UI.RawUI.BackgroundColor)"
        } else {
            $contentColor = "$($host.UI.RawUI.ForegroundColor)","$($host.UI.RawUI.BackgroundColor)"
        }
        $contentLengthLength = $contentLength.Length
        $numRowWidth = ($numRowWidthSides*2)+$contentLengthLength
        [int]$contentSpaceWidth = $host.UI.RawUI.BufferSize.Width - $numRowWidth - $dividerWidth - $offsetWidth
        # Prep
        [string]$topBar = "$horizontalLine"*$numRowWidth
        $topBar += "$topDivider"*$dividerWidth
        $topBar += "$horizontalLine"*$contentSpaceWidth
        [string]$midBar = "$horizontalLine"*$numRowWidth
        $midBar += "$midDivider"*$dividerWidth
        $midBar += "$horizontalLine"*$contentSpaceWidth
        [string]$bottomBar = "$horizontalLine"*$numRowWidth
        $bottomBar += "$bottomDivider"*$dividerWidth
        $bottomBar += "$horizontalLine"*$contentSpaceWidth
        [string]$numRowEmpty = " "*$numRowWidth
        [string]$horizontalOffsetString = " "*$contentOffsetHorizontal

        # Print header
        write-host $topBar -f $linesColor[0] -b $linesColor[1]
        write-host $numRowEmpty -NoNewline
        write-host $verticalLine -NoNewline -f $linesColor[0] -b $linesColor[1]
        write-host $horizontalOffsetString -NoNewline
        write-host "File: $file    " -f $contentColor[0] -b $contentColor[1] -NoNewline
        if ($filetype -or $fileassoc) { write-host "(" -f "DarkGray" -b $contentColor[1] -NoNewline }
        if ($filetype) { write-host "Filetype: $filetype" -f "DarkGray" -b $contentColor[1] -NoNewline }
        if ($filetype -and $fileassoc) { write-host "   " -NoNewline }
        if ($fileassoc) { write-host "WinFileAssoc: $fileAssoc" -f "DarkGray" -b $contentColor[1] -NoNewline }
        if ($filetype -or $fileassoc) { write-host ")" -f "DarkGray" -b $contentColor[1]} else { write-host "" }
        write-host $midBar -f $linesColor[0] -b $linesColor[1]
        # Vertical Offset
        if ($contentOffsetVertical -gt 0) {
            write-host $numRowEmpty -NoNewline
            write-host $verticalLine -NoNewline -f $linesColor[0] -b $linesColor[1]
            write-host $horizontalOffsetString -NoNewline
            write-host ""
        }
        # Print file contents
        $c = 0
        foreach ($_ in $content) {
            $c++
            if ($contentLength -eq "0") {$c = " "}
            $endOffset = $numRowWidthSides
            [int]$lle = "$c".length
            if ($lle -eq 2) {$endOffset = $endOffset - 1} elseif ($lle -eq 3) {$endOffset = $endOffset - 2}
            write-host "$(" "*$numRowWidthSides)" -NoNewline
            write-host $c -NoNewline -f $linesColor[0] -b $linesColor[1]
            write-host "$(" "*$endOffset)" -NoNewline
            write-host $verticalLine -NoNewline -f $linesColor[0] -b $linesColor[1]
            write-host $horizontalOffsetString -NoNewline
            if ($contentLength -eq "0") { write-host "Empty file." -f $linesColor[0] -b $linesColor[1] } else {
                write-host $content[$c-1] -f $contentColor[0] -b $contentColor[1]
            }
        }
        # Vertical Offset
        if ($contentOffsetVertical -gt 0) {
            write-host $numRowEmpty -NoNewline
            write-host $verticalLine -NoNewline -f $linesColor[0] -b $linesColor[1]
            write-host $horizontalOffsetString -NoNewline
            write-host ""
        }
        # Write footer
        write-host $bottomBar -f $linesColor[0] -b $linesColor[1]
    } else {
        return "`e[31mFile not found!`e[0m"
    }
} else { return "`e[31mFile can't be null!`e[0m" }