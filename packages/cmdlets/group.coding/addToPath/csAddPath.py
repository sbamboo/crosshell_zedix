import os
y = inputs("Are you sure? (if so answear al caps!)")
if y == "YES":
    if IsWindows() == True:
        patha = f"{csbasedir}{os.sep}.path"
        pwshScript = os.path.realpath(f"{os.path.dirname(path)}{os.sep}.add.ps1")
        os.system(f"pwsh -File {pwshScript} '{patha}'")
else:
    print("OperationQuit")