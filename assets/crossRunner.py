# [Imports]
import sys
import subprocess
import os
import ast
from assets.evaluate import *
from assets.longPATHhandler import string_allowed

# [Setup Functions]
# Function to autodecode cp437
def handle_cp437(bytestring):
    try:
        decoded_string = bytestring.decode('cp437')
    except UnicodeDecodeError:
        decoded_string = string
    return decoded_string

# Function to start a shell with or without STDOUT capturing
def runShell(main=str(),captureOutput=False,params=list(),cmd=list()):
    if string_allowed(' '.join([main, *cmd, *params])) == False:
        return "error.runshellExeception.WINLONGPATHDISABLED_COMMANDTOLONG"
    # Check captureOutput and if disabled just execute a subprocess
    if captureOutput == False:
        subprocess.run([f'{main}', *cmd, *params], stderr=sys.stderr, stdout=sys.stdout)
    # If enabled launch a subprocess which captures output to a subprocess.PIPE stream-object
    else:
        # 1: Execute the shell and it's paramaters, 2: Get the communicateObject at index 1 for the STDOUT and return the out with the upper function.
        proc = subprocess.Popen([f'{main}', *cmd, *params], stderr=sys.stderr, stdout=subprocess.PIPE)
        out = proc.communicate()[0]
        out = handle_cp437(out)
        return out.upper()

# [Runners]
# Function to run a powershell script without without variable/command/function passing
def Powershell(inputs,params,sendVars=False,varDict=None,passBackVars=False,legacyNames=False,allowFuncCalls=False,captureOutput=False):
    # Check inputs and replace double path separators.
    inputs = os.path.realpath(inputs)
    inputs = inputs.replace("\\\\", "\\")
    inputs = inputs.replace("//", "/")
    # Get the path of the crossRunner
    fp = os.path.realpath(__file__)
    fps = fp.split(os.sep)
    fps.pop(-1)
    fp2 = ""
    # For each element in the path (folder) handle sepparators
    for elem in fps:
        fp2 += f"§{elem}"
    fp2 = fp2.strip("§")
    fp2 = fp2.replace("§",os.sep)
    # Add the support folder to the path
    fp2 += os.sep + "support"
    # Continue and check if the function should send variables to the powershell subprocess. And if not execute the code bellow
    if sendVars == False:
        # Also check if the function should capture output and if so capture it to the capture output variable
        if captureOutput == True:
            # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
            capturedOutput = runShell("pwsh",captureOutput,[inputs, *params])
        else:
            # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
            capturedOutput = runShell("pwsh",captureOutput,[inputs, *params])
    # If the script should send variables do the following:
    else:
        # Handle variable Dictionary
        vars = str()
        # Enumerate through the dictionary
        for i,key in enumerate(varDict):
            # Remove <function> elements
            if not "<function" in str(varDict[key]) and not "__" in str(key):
                # Add a placeholder parsed string to vars
                vars += f"{key}§{varDict[key]}§¤§"
        # Strip placeholder from end of string
        vars.rstrip("§¤§")
        # Run the script but first if crosshell is running on linux fix the path
        if IsLinux(): 
            if str(fp2)[0] != str(os.sep): fp2 = os.sep + fp2
        # Setup som filepaths
        runtime = f"{fp2}{os.sep}runtime.ps1"
        runtime = os.path.realpath(runtime)
        exitFile = str(os.path.realpath(f"{fp2}{os.sep}exit.empty"))
        passbackFile = str(os.path.realpath(f"{fp2}{os.sep}passback.vars"))
        funcCallFile = str(os.path.realpath(f"{fp2}{os.sep}passback.calls"))
        # If an exitfile exists remove it
        if os.path.exists(exitFile) == True:
            os.remove(exitFile)
        # If captureOuput is true run the runtime script with the correct parameters and capture the output
        if captureOutput == True:
            # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
            capturedOutput = runShell("pwsh",captureOutput,params,[runtime,f"{inputs}",f'{vars}',f'{passBackVars}',f"{legacyNames}",f"{allowFuncCalls}"])
        # Otherwise just run the runtime script
        else:
            # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
            capturedOutput = runShell("pwsh",captureOutput,params,[runtime,f"{inputs}",f'{vars}',f'{passBackVars}',f"{legacyNames}",f"{allowFuncCalls}"])
        # Check if the function should wait for the runtime to send back variables
        if passBackVars == True:
            # While loop to wait for a passbackfile
            while True:
                # If allowFuncCalls is enabled contunisly check for functionCalls
                if os.path.exists(funcCallFile) == True:
                    # Try getting the content
                    try:
                        content = open(funcCallFile, "r").read()
                        content = content.rstrip("\n")
                    except:
                        content = ""
                    # remove a funcCallFile
                    os.remove(funcCallFile)
                    # Handle decode atempt
                    if "{%1%}" in content or "{%2%}" in content:
                        content = str(content) + "-decode"
                    # Send call to function using the cs_execInput
                    # cs_execInput(<command>)
                    cs_execInput(content)
                # If a variablePassbackFile exists break the loop
                if os.path.exists(passbackFile) == True:
                    break
            # Get content from variable passback file
            content = open(passbackFile,"r",encoding="utf-8").read()
            # Remove variable passbackFile
            os.remove(passbackFile)
            # Parse out the runtimes passback string
            passBacks = content.split("§¤§")
            # Remove empty last element
            if passBacks[-1] == "": passBacks.pop(-1)
            # Iterate through out the variables and parse out name and value
            for var in passBacks:
                if var != "" and var != "\n":
                    name = var.split("§")[0]
                    value = var.replace(f"{name}§","")
                    # If the name starts with a ! dont eval the value and just add it
                    if name[0] == "!":
                        name = name.lstrip("!")
                        varDict[name] = value.strip("'")
                    # If no !, literal_eval the inpu and then add it to the variable Dictionary
                    else:
                        # Check if value is string and if so add "" to help literal_eval
                        if str(value)[0] != "[" and str(value)[0] != '"': value = '"' + str(value) + '"'
                        value2 = ast.literal_eval(value)
                        varDict[name] = value2
    # if a exit.empty file exists remove it
    if os.path.exists(f"{fp2}{os.sep}exit.empty"):
        os.remove(f"{fp2}{os.sep}exit.empty")
    # If input has been captured return it othervise just return the new variables
    if "error.runshellExeception" in str(capturedOutput): return varDict,capturedOutput
    if captureOutput == True:
        return varDict,capturedOutput
    else:
        return varDict,False

# Function to run bat/cmd files
def batCMD(path,params,captureOutput=False):
    # If capture output is enabled, capture STDOUT and return it
    if captureOutput == True:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell("cmd",captureOutput,["/c", path, *params])
        return capturedOutput
    else:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell("cmd",captureOutput,["/c", path, *params])
        if "error.runshellExeception" in str(capturedOutput): return capturedOutput
        return False

# Function to run exe files
def winEXE(path,params,captureOutput=False):
    # If capture output is enabled, capture STDOUT and return it
    if captureOutput == True:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell(path,captureOutput,[*params])
        return capturedOutput
    else:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell(path,captureOutput,[*params])
        if "error.runshellExeception" in str(capturedOutput): return capturedOutput
        return False

# Function to run platform executables / binaries
def platformExe(path,params,captureOutput=False):
    # If capture output is enabled, capture STDOUT and return it
    if captureOutput == True:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell(path,captureOutput,[*params])
        return capturedOutput
    else:
        # runShell(<shell>,<captureOutput-bool>,<list-of-inputs-and-other-parameters>)
        capturedOutput = runShell(path,captureOutput,[*params])
        if "error.runshellExeception" in str(capturedOutput): return capturedOutput
        return False