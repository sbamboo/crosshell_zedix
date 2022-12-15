function Show-Tree_license {
    write-host "MIT License`n`nCopyright (c) 2017-2022 JDH Information Technology Solutions, Inc.`n`n`nPermission is hereby granted, free of charge, to any person obtaining a copy`nof this software and associated documentation files (the "Software"), to deal`nin the Software without restriction, including without limitation the rights`nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell`ncopies of the Software, and to permit persons to whom the Software is`nfurnished to do so, subject to the following conditions:`n`n`nThe above copyright notice and this permission notice shall be included in`nall copies or substantial portions of the Software.`n`n`nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR`nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,`nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE`nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER`nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,`nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN`nTHE SOFTWARE."
}

function Show-Tree {
    # Original script is from: https://raw.githubusercontent.com/jdhitsolutions/PSScriptTools/master/functions/ShowTree.ps1
    # But has been modified to allow the use of other characters, modifications were made by: Simon Kalmi Claesson
    # 

    [CmdletBinding(DefaultParameterSetName = "Path")]
    [alias("pstree","shtree")]

    Param(
        [Parameter(Position = 0,
            ParameterSetName = "Path",
            ValueFromPipeline,
            ValueFromPipelineByPropertyName
            )]
        [ValidateNotNullOrEmpty()]
        [alias("FullName")]
        [string[]]$Path = ".",

        [Parameter(Position = 0,
            ParameterSetName = "LiteralPath",
            ValueFromPipelineByPropertyName
            )]
        [ValidateNotNullOrEmpty()]
        [string[]]$LiteralPath,

        [Parameter(Position = 1)]
        [ValidateRange(0, 2147483647)]
        [int]$Depth = [int]::MaxValue,

        [Parameter()]
        [ValidateRange(1, 100)]
        [int]$IndentSize = 3,

        [Parameter()]
        [alias("f","files")]
        [switch]$ShowItem,

        [Parameter()]
        [alias("char2","extendedcharset","extcharset","extset","ext","e")]
        [switch]$extchar,

        [Parameter()]
        [switch]$emoji,

        [Parameter(HelpMessage = "Display item properties. Use * to show all properties or specify a comma separated list.")]
        [alias("properties")]
        [string[]]$ShowProperty,

        [string]$charset
    )
    DynamicParam {
        #define the InColor parameter if the path is a FileSystem path
        if ($PSBoundParameters.containsKey("Path")) {
            $here = $psboundParameters["Path"]
        }
        elseif ($PSBoundParameters.containsKey("LiteralPath")) {
            $here = $psboundParameters["LiteralPath"]
        }
        else {
            $here = (Get-Location).path
        }
       if (((Get-Item -path $here).PSprovider.Name -eq 'FileSystem' )-OR ((Get-Item -literalpath $here).PSprovider.Name -eq 'FileSystem')) {

            #define a parameter attribute object
            $attributes = New-Object System.Management.Automation.ParameterAttribute
            $attributes.HelpMessage = "Show tree and item colorized."

            #add an alias
            $alias = [System.Management.Automation.AliasAttribute]::new("ansi")

            #define a collection for attributes
            $attributeCollection = New-Object -Type System.Collections.ObjectModel.Collection[System.Attribute]
            $attributeCollection.Add($attributes)
            $attributeCollection.Add($alias)

            #define the dynamic param
            $dynParam1 = New-Object -Type System.Management.Automation.RuntimeDefinedParameter("InColor", [Switch], $attributeCollection)

            #create array of dynamic parameters
            $paramDictionary = New-Object -Type System.Management.Automation.RuntimeDefinedParameterDictionary
            $paramDictionary.Add("InColor", $dynParam1)
            #use the array
            return $paramDictionary
       }
    } #DynamicParam

    Begin {
        Write-Verbose "Starting $($myinvocation.MyCommand)"
        if (-Not $Path -and $psCmdlet.ParameterSetName -eq "Path") {
            $Path = Get-Location
        }

        if ($PSBoundParameters.containskey("InColor") -or $PSBoundParameters.containskey("Emoji")) {
            $Colorize = $True
            $script:top = ($global:PSAnsiFileMap).where( {$_.description -eq 'TopContainer'}).Ansi
            $script:child = ($global:PSAnsiFileMap).where( {$_.description -eq 'ChildContainer'}).Ansi
        }
        function GetIndentString {
            [CmdletBinding()]
            Param([bool[]]$IsLast)

            #Handle Extended CharacterSet, and customized character sets.
            if ($emoji) {$extchar = $True}
            if ($extchar) {
                if ($charset) {
                  #Format for custom character sets: "+;\;|;-"
                  [array]$charsetA = $charset -split ";"
                  $C2_inclChar = $charsetA[0]
                  $C2_endiChar = $charsetA[1]
                  $C2_vertChar = $charsetA[2]
                  $C2_lineChar = $charsetA[3]
                } else {
                  $C2_inclChar = "├"
                  $C2_endiChar = "└"
                  $C2_vertChar = "│"
                  $C2_lineChar = "─"
                }
            } else {
                $C2_inclChar = "+"
                $C2_endiChar = "\"
                $C2_vertChar = "|"
                $C2_lineChar = "-"
            }

            Write-Verbose "Starting $($myinvocation.MyCommand)"
            #  $numPadChars = 1
            $str = ''
            for ($i = 0; $i -lt $IsLast.Count - 1; $i++) {
                $sepChar = if ($IsLast[$i]) {' '} else {"$C2_vertChar"}
                $str += "$sepChar"
                $str += " " * ($IndentSize - 1)
            }

            #The \ indicates the item is the last in the container
            $teeChar = if ($IsLast[-1]) {"$C2_endiChar"} else {"$C2_inclChar"}
            $str += "$teeChar"
            $str += "$C2_lineChar" * ($IndentSize - 1)
            $str

            Write-Verbose "Ending $($myinvocation.MyCommand)"
        }

        function ShowProperty() {
            [cmdletbinding()]
            Param(
                [string]$Name,
                [string]$Value,
                [bool[]]$IsLast
            )
            Write-Verbose "Starting $($myinvocation.MyCommand)"
            $indentStr = GetIndentString $IsLast
            $propStr = "${indentStr} $Name = "
            $availableWidth = $host.UI.RawUI.BufferSize.Width - $propStr.Length - 1
            if ($Value.Length -gt $availableWidth) {
                $ellipsis = '...'
                $val = $Value.Substring(0, $availableWidth - $ellipsis.Length) + $ellipsis
            }
            else {
                $val = $Value
            }
            $propStr += $val
            $propStr
            Write-Verbose "Ending $($myinvocation.MyCommand)"
        }
        function ShowItem {
            [CmdletBinding()]
            Param(
                [string]$Path,
                [string]$Name,
                [bool[]]$IsLast,
                [bool]$HasChildItems = $false,
                [switch]$Color,
                [ValidateSet("topcontainer","childcontainer","file")]
                [string]$ItemType
            )
            Write-Verbose "Starting $($myinvocation.MyCommand)"
            $PSBoundParameters | Out-String | Write-Verbose
            if ($IsLast.Count -eq 0) {
                if ($Color) {
                    Write-Output "$([char]0x1b)[38;2;0;255;255m$("$(Resolve-Path $Path)")$([char]0x1b)[0m"
                    # Write-Output "$($script:top)$("$(Resolve-Path $Path)")$([char]0x1b)[0m"

                }
                else {
                    "$(Resolve-Path $Path)"
                }
            }
            else {
                $indentStr = GetIndentString $IsLast
                if ($Color) {
                    if ($emoji) {
                            #ToDo - define a user configurable color map
                            $indentStr = $indentStr.Substring(0,$indentStr.Length-1)
                            Switch ($ItemType) {
                                "topcontainer" {
                                    #Write-Output "$indentStr$($script:top)$($Name)$([char]0x1b)[0m"
                                    Write-Output "$indentStr📁$([char]0x1b)[38;2;0;255;255m$("$Name")$([char]0x1b)[0m"
                                }
                                "childcontainer" {
                                    #Write-Output "$indentStr$($script:child)$($Name)$([char]0x1b)[0m"
                                    Write-Output "$indentStr📁$([char]0x1b)[38;2;255;255;0m$("$Name")$([char]0x1b)[0m"
                                }
                                "file" {
    
                                    #only use map items with regex patterns
                                    foreach ($item in ($global:PSAnsiFileMap | Where-object Pattern)) {
                                        if ($name -match $item.pattern -AND (-not $done)) {
                                            write-Verbose "Detected a $($item.description) file"
                                            Write-Output "$indentStr📄$($item.ansi)$($Name)$([char]0x1b)[0m"
                                            #set a flag indicating we've made a match to stop looking
                                            $done = $True
                                        }
                                    }
                                    #no match was found so just write the item.
                                    if (-Not $done) {
                                        write-verbose "No ansi match for $Name"
                                        #Write-Output "$indentStr$Name$([char]0x1b)[0m"
                                        Write-Output "$indentStr📄$([char]0x1b)[34m$Name$([char]0x1b)[0m"
                                    }
                                } #file
                                Default {
                                    Write-Output "$indentStr$Name"
                                }
                            } #switch
                    } else {
                        #ToDo - define a user configurable color map
                        Switch ($ItemType) {
                            "topcontainer" {
                                #Write-Output "$indentStr$($script:top)$($Name)$([char]0x1b)[0m"
                                Write-Output "$indentStr$([char]0x1b)[38;2;0;255;255m$("$Name")$([char]0x1b)[0m"
                            }
                            "childcontainer" {
                                #Write-Output "$indentStr$($script:child)$($Name)$([char]0x1b)[0m"
                                Write-Output "$indentStr$([char]0x1b)[38;2;255;255;0m$("$Name")$([char]0x1b)[0m"
                            }
                            "file" {

                                #only use map items with regex patterns
                                foreach ($item in ($global:PSAnsiFileMap | Where-object Pattern)) {
                                    if ($name -match $item.pattern -AND (-not $done)) {
                                        write-Verbose "Detected a $($item.description) file"
                                        Write-Output "$indentStr$($item.ansi)$($Name)$([char]0x1b)[0m"
                                        #set a flag indicating we've made a match to stop looking
                                        $done = $True
                                    }
                                }
                                #no match was found so just write the item.
                                if (-Not $done) {
                                    write-verbose "No ansi match for $Name"
                                    #Write-Output "$indentStr$Name$([char]0x1b)[0m"
                                    Write-Output "$indentStr$([char]0x1b)[34m$Name$([char]0x1b)[0m"
                                }
                            } #file
                            Default {
                                Write-Output "$indentStr$Name"
                            }
                        } #switch
                    }
                } #if color
                else {
                    "$indentStr$Name"
                }
            }

            if ($ShowProperty) {
                $IsLast += @($false)

                $excludedProviderNoteProps = 'PSChildName', 'PSDrive', 'PSParentPath', 'PSPath', 'PSProvider'
                $props = @(Get-ItemProperty $Path -ea 0)
                if ($props[0] -is [pscustomobject]) {
                    if ($ShowProperty  -eq "*") {
                        $props = @($props[0].psobject.properties | Where-object {$excludedProviderNoteProps -notcontains $_.Name })
                    }
                    else {
                        $props = @($props[0].psobject.properties |
                        Where-object {$excludedProviderNoteProps -notcontains $_.Name -AND $showproperty -contains $_.name})
                    }
                }

                for ($i = 0; $i -lt $props.Count; $i++) {
                    $prop = $props[$i]
                    $IsLast[-1] = ($i -eq $props.count - 1) -and (-Not $HasChildItems)
                    $showParams = @{
                        Name = $prop.Name
                        Value = $prop.Value
                        IsLast = $IsLast
                    }
                    ShowProperty @showParams
                }
            }
            Write-Verbose "Ending $($myinvocation.MyCommand)"
        }

        function ShowContainer {
            [CmdletBinding()]
            Param (
                [string]$Path,
                [string]$Name = $(Split-Path $Path -Leaf),
                [bool[]]$IsLast = @(),
                [switch]$IsTop,
                [switch]$Color
            )

            Write-Verbose "Starting $($myinvocation.MyCommand) on $Path"
            $PSBoundParameters | Out-String | Write-Verbose
            if ($IsLast.Count -gt $Depth) { return }

            $childItems = @()
            if ($IsLast.Count -lt $Depth) {
                try {
                    $rpath = Resolve-Path -literalpath $Path -ErrorAction stop
                }
                catch {
                    Throw "Failed to resolve $path. This PSProvider and path may be incompatible with this command."
                    #bail out
                    return
                }
                $childItems = @(Get-ChildItem $rpath -ErrorAction $ErrorActionPreference |
                        Where-object {$ShowItem -or $_.PSIsContainer})
            }
            $hasChildItems = $childItems.Count -gt 0

            # Show the current container
            $sParams = @{
                path          = $Path
                name          = $Name
                IsLast        = $IsLast
                hasChildItems = $hasChildItems
                Color         = $Color
                ItemType      =  If ($isTop) {"topcontainer"} else {"childcontainer"}
            }
            ShowItem @sParams

            # Process the children of this container
            $IsLast += @($false)
            for ($i = 0; $i -lt $childItems.count; $i++) {
                $childItem = $childItems[$i]
                $IsLast[-1] = ($i -eq $childItems.count - 1)
                if ($childItem.PSIsContainer) {
                    $iParams = @{
                        path   = $childItem.PSPath
                        name   = $childItem.PSChildName
                        isLast = $IsLast
                        Color  = $color
                    }
                    ShowContainer @iParams
                }
                elseif ($ShowItem) {
                    $unresolvedPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($childItem.PSPath)
                    $name = Split-Path $unresolvedPath -Leaf
                    $iParams = @{
                        Path   = $childItem.PSPath
                        Name   = $name
                        IsLast = $IsLast
                        Color  = $Color
                       ItemType = "File"
                    }
                    ShowItem @iParams
                }
            }
            Write-Verbose "Ending $($myinvocation.MyCommand)"
        }
    } #begin

    Process {
        Write-Verbose "Detected parameter set $($pscmdlet.ParameterSetName)"
        if ($psCmdlet.ParameterSetName -eq "Path") {
            # In the -Path (non-literal) resolve path in case it is wildcarded.
            $resolvedPaths = @($Path | Resolve-Path | Foreach-object {$_.Path})
        }
        else {
            # Must be -LiteralPath
            $resolvedPaths = @($LiteralPath)
        }
        Write-Verbose "Using these PSBoundParameters"
        $PSBoundParameters | Out-String | Write-Verbose

        foreach ($rpath in $resolvedPaths) {
            Write-Verbose "Processing $rpath"
            $showParams = @{
                Path  = $rpath
                Color = $colorize
                IsTop = $True
            }
            ShowContainer @showParams
          }
    } #process
    end {
        Write-Verbose "Ending $($myinvocation.MyCommand)"
    }
}