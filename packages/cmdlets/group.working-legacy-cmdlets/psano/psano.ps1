<#
  .SYNOPSIS
  Import of David's PSano module.
#>
$old_path = $pwd
cd $psscriptroot\.module
$NestedModules = @('.\1KeyEvents\1KeyHandle.ps1', 
               '.\1KeyEvents\2KeyHandler.ps1', 
               '.\1KeyEvents\FocusSwitchingHandle.ps1', 
               '.\2UI\1Point.ps1', 
               '.\2UI\2Canvas.ps1', 
               '.\2UI\3Panel.ps1', 
               '.\2UI\4Form.ps1', 
               '.\private\1BufferPanel.ps1', 
               '.\private\BufferEditor.ps1', 
               '.\private\Headerpanel.ps1', 
               '.\private\MenuPanel.ps1', 
               '.\private\PSanoFile.ps1', 
               '.\private\PSanoFileInSession.ps1', 
               '.\private\PSanoFunction.ps1', 
               '.\private\PSanoVariable.ps1', 
               '.\private\RemoveEvent.ps1', 
               '.\Public\Aliases.ps1', 
               '.\Public\New-PSanoInstance.ps1')

foreach ($f in $nestedmodules) {. $f}
$c = "Edit-TextFile " + $args
if ($c -notlike "*;*") {iex($c)}
cd $old_path