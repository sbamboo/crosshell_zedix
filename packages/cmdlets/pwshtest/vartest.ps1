# [CStags]
# pwsh.passCSvars: True
# pwsh.returnCSVars: True
# pwsh.allowFuncCalls: True
# [TagEnd]
$csshell_prefix = ">> "
# Export variables
. "$script:cs_runtime_loc\pwsh_functionCaller.ps1" "prefix -reset"
. "$script:cs_runtime_loc\pwsh_exportVariables.ps1" "csshell_prefix"