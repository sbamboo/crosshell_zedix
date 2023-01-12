<#
  .SYNOPSIS
  Import of Brandon Wood's piglet module.
#>
param(
  [Parameter(Position=0, Mandatory=$true, ValueFromPipeline=$true)]
  [String]
  $Text,

  [String]
  $Font = "standard",

  [ValidateSet("Black", "Blue", "Cyan", "DarkBlue", "DarkCyan", "DarkGray", 
         "DarkGreen", "DarkMagenta", "DarkRed", "DarkYellow", "Gray", 
         "Green", "Magenta", "Rainbow", "Red", "White", "Yellow")]
  [Alias('f')]
  [String] $ForegroundColor = "Default",

  [ValidateSet("Black", "Blue", "Cyan", "DarkBlue", "DarkCyan", "DarkGray",
         "DarkGreen", "DarkMagenta", "DarkRed", "DarkYellow", "Gray", 
         "Green", "Magenta", "Red", "White", "Yellow")]
  [Alias('b')]
  [String] $BackgroundColor = "Default"
    )

Import-Module -force $psscriptroot\piglet.psm1
piglet @PSBoundParameters