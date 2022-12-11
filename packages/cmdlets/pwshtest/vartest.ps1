# [CStags]
# pwsh.passCSvars: True
# pwsh.returnCSVars: True
# [TagEnd]
$csshell_prefix = ">> "
# Export variables
. "$script:cs_runtime_loc\pwsh_exportVariables.ps1" "csshell_prefix"