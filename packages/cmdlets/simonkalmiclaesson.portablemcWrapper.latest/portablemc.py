# [Imports]
import os
hasinstalledState = f"{CSScriptRoot}{os.sep}hasinstalled.empty"
if not os.path.exists(hasinstalledState):
    print("Installing portablemc...")
    os.system("python3 -m pip install --user portablemc")
    os.system("python3 -m pip install --user portablemc-fabric")
    os.system("python3 -m pip install --user portablemc-forge")
    os.system("python3 -m pip install --user portablemc-quilt")
    outFile("1",hasinstalledState)

# [Run portable mc]
commandString = "python3 -m portablemc " + (' '.join(argv)).strip(" ")
os.system(commandString)
