# This file is depricated

from assets.coreFuncs import *
from assets.shellFuncs import *

def cs_evalAndRun(inputs=str(),varDict=dict()):
    allowedFileTypes = varDict["allowedFileTypes"]
    cspathables = varDict["cspathables"]
    # Has pipes
    if " | " in inputs:
        hasPipes = True
        pipeParts = inputs.split(" | ")
    else:
        hasPipes = False
        pipeParts = [inputs]
    # handle pipes
    pipeSTDOUT = ""
    for pipeIndex,pipePart in enumerate(pipeParts):
        # Handle parantheses
        if "(" in pipePart and " " not in pipePart:
            pipePart = pipePart.replace("("," ")
            pipePart = pipePart.replace(")"," ")
            pipePart = pipePart.replace(","," ")
        partials = pipePart.split(" ")
        cmd = partials[0]
        params = partials[1:]
        # Reload command
        if cmd == "reload":
            cspathables = cs_loadCmdlets("./packages/cmdlets",allowedFileTypes)
        # Restart command
        #elif cmd == "restart":
        #    path = csbasedir + os.sep + "zedix.py"
        #    exec(open(path).read(), globals())
        # cs.getPathables Command
        elif cmd == "cs.getPathables":
            for i in cspathables:
                d = i.split(";")
                d[0] = d[0].replace(':"',': "')
                print(f"\033[33m{d[0]}\033[0m")
                for i in range(1,len(d)):
                    d[i] = d[i].replace(':"',': "')
                    d[i] = d[i].replace(':[',': [')
                    print(f"   \033[32m{d[i]}\033[0m")
                print("")
        # Al other commands
        elif cmd != "":
            if "Info:" in cs_builtins(cmd,allowedFileTypes):
                path = cs_getPathablePath(cspathables,cmd)
                if "Error:" in path:
                    print(path)
                else:
                    # Excute
                    if hasPipes == False:
                        cs_exec(path,params,globals(),False)
                    else:
                        # Handle unnice pipeElems in pipeSTDOUT
                        if "b'" in str(pipeSTDOUT):
                            str_pipeSTDOUT = str(pipeSTDOUT)
                            str_pipeSTDOUT = str_pipeSTDOUT.strip("b'")
                            str_pipeSTDOUT= str_pipeSTDOUT.rstrip("'")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\n","\n")
                            str_pipeSTDOUT = str_pipeSTDOUT.replace("\\r","\r")
                            pipeSTDOUT = str_pipeSTDOUT
                        # Handle pipeSTDOUT
                        if pipeSTDOUT != "" and pipeSTDOUT != None:
                            params = [pipeSTDOUT, *params]
                        if pipeIndex != (len(pipeParts)-1):
                            pipeSTDOUT = cs_exec(path,params,globals(),True)
                        else:
                            cs_exec(path,params,globals(),False)