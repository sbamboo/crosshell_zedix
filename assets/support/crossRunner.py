import sys
import subprocess
import os
import ast

# [Setup]
def runShell(main=str(),captureOutput=False,params=list(),cmd=list()):
    if captureOutput == False:
        subprocess.run([f'{main}', *cmd, *params], stderr=sys.stderr, stdout=sys.stdout)
    else:
        proc = subprocess.Popen([f'{main}', *cmd, *params], stderr=sys.stderr, stdout=subprocess.PIPE)
        out = proc.communicate()[0]
        return out.upper()

# [Runners]
def Powershell(inputs,params,sendVars=False,varDict=None,passBackVars=False,legacyNames=False,captureOutput=False):
    inputs = os.path.realpath(inputs)
    inputs = inputs.replace("\\\\", "\\")
    inputs = inputs.replace("//", "/")
    # FPS
    fp = os.path.realpath(__file__)
    fps = fp.split(os.sep)
    fps.pop(-1)
    fp2 = ""
    for elem in fps:
        fp2 += f"§{elem}"
    fp2 = fp2.strip("§")
    fp2 = fp2.replace("§",os.sep)
    # Continue
    if sendVars == False:
        if captureOutput == True:
            capturedOutput = runShell("pwsh",captureOutput,[inputs, *params])
        else:
            runShell("pwsh",captureOutput,[inputs, *params])
    else:
        # Handle varDict
        vars = str()
        for i,key in enumerate(varDict):
            if not "<function" in str(varDict[key]) and not "__" in str(key):
                vars += f"{key}§{varDict[key]}§¤§"
        vars.rstrip("§¤§")
        # Run
        runtime = f"{fp2}{os.sep}runtime.ps1"
        runtime = os.path.realpath(runtime)
        exitFile = str(os.path.realpath(f"{fp2}{os.sep}exit.empty"))
        passbackFile = str(os.path.realpath(f"{fp2}{os.sep}passback.vars"))
        if os.path.exists(exitFile) == True:
            os.remove(exitFile)
        if captureOutput == True:
            capturedOutput = runShell("pwsh",captureOutput,params,[runtime,f"{inputs}",f'{vars}',f'{passBackVars}',f"{legacyNames}"])
        else:
            runShell("pwsh",captureOutput,params,[runtime,f"{inputs}",f'{vars}',f'{passBackVars}',f"{legacyNames}"])
        if passBackVars == True:
            while True:
                if os.path.exists(passbackFile) == True:
                    break
            content = open(passbackFile,"r",encoding="utf-8").read()
            os.remove(passbackFile)
            passBacks = content.split("§¤§")
            if passBacks[-1] == "": passBacks.pop(-1)
            for var in passBacks:
                if var != "" and var != "\n":
                    name = var.split("§")[0]
                    value = var.replace(f"{name}§","")
                    if name[0] == "!":
                        name = name.lstrip("!")
                        varDict[name] = value.strip("'")
                    else:
                        if str(value)[0] != "[" and str(value)[0] != '"': value = '"' + str(value) + '"'
                        value2 = ast.literal_eval(value)
                        varDict[name] = value2
    if os.path.exists(f"{fp2}{os.sep}exit.empty"):
        os.remove(f"{fp2}{os.sep}exit.empty")
    if captureOutput == True:
        return varDict,capturedOutput
    else:
        return varDict,False

def batCMD(path,params,captureOutput=False):
    if captureOutput == True:
        capturedOutput = runShell("cmd",captureOutput,["/c", path, *params])
        return capturedOutput
    else:
        runShell("cmd",captureOutput,["/c", path, *params])
        return False


def winEXE(path,params,captureOutput=False):
    if captureOutput == True:
        capturedOutput = runShell(path,captureOutput,[*params])
        return capturedOutput
    else:
        runShell(path,captureOutput,[*params])
        return False