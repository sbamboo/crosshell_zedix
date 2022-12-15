# Main functions for the zedix core
# Author: Simon Kalmi Claesson

from assets.utils.utilFuncs import *
from assets.coreFuncs import *
import assets.crossRunner as cse
import os
import sys
from io import StringIO
import yaml
import json

def cs_loadCmdlets(Path=str(),allowedFileTypes=list()):
    pathables = []
    if allowedFileTypes == []:
        allowedFileTypes = [".py"]
    entries = scantree(Path)
    for file in entries:
        fending = str("." +''.join(file.path.split('.')[-1]))
        valid = True
        for elem in os.path.realpath(str(file.path)).split(os.sep):
            if str(elem) != "":
                if str(elem)[0] == ".":
                    valid = False
        if not ".cfg" in fending and file.name[0] != "." and fending in allowedFileTypes and os.path.isfile(file.path) == True and valid == True:
            # Handle path
            fpath = file.path
            fpath = fpath.replace('/',os.sep).replace('\\',os.sep)
            # Handle name
            fname = file.name
            fname = fname.replace(fname.split('.')[-1],"").strip('.')
            # Handle other properties
            fconfigfile =  fpath.replace(fending,".cfg")
            faliases = "[]"
            if os.path.exists(fconfigfile):
                fconfig = readConfig(fconfigfile)
                # config
                if fconfig.get("pathoverwrite") != "" and fconfig.get("pathoverwrite") != '""':
                    fpath = fconfig.get("pathoverwrite")
                    fpath = fpath.replace("{cmdletsFolder}",Path)
                if fconfig.get("nameoverwrite") != "" and fconfig.get("nameoverwrite") != '""':
                    fname = fconfig.get("nameoverwrite")
                if fconfig.get("aliases") != "" and fconfig.get("aliases") != '[]':
                    faliases = fconfig.get("aliases")
                if fconfig.get("description") != "" and fconfig.get("description") != '""':
                    fdescription = fconfig.get("description")
                if fconfig.get("paramhelp") != "" and fconfig.get("paramhelp") != '""':
                    fparamhelp = fconfig.get("paramhelp")
                if fconfig.get("blockCommonparams") != "" and fconfig.get("blockCommonparams") != '""':
                    fblockCommonparams = fconfig.get("blockCommonparams")
                if fconfig.get("synopsisDesc") != "" and fconfig.get("synopsisDesc") != '""':
                    fsynopsisDesc = fconfig.get("synopsisDesc")
                if fsynopsisDesc == "True":
                    if fending == ".ps1":
                        raw_content = open(os.path.realpath(fpath),"r").read()
                        split_content = raw_content.split("\n")
                        o_fdesc = fdescription
                        try:
                            if str(split_content[0]).strip() == "<#" and str(split_content[1]).strip() == ".SYNOPSIS":
                                fdescription = str(split_content[2]).strip()
                        except:
                            fdescription = o_fdesc
            # Add to pathables
            pathables.append(f'name:"{fname}";path:"{fpath}";aliases:{faliases};description:"{fdescription}";paramhelp:"{fparamhelp}";blockCommonParameters:"{fblockCommonparams}";synopsisDesc{fsynopsisDesc}')
            fname,fpath,faliases,fdescription,fparamhelp = str(),str(),str('[]'),str(),str()
    return pathables

def cs_getPathableProperties(pathData=str()):
    splitData = list(pathData.split(';'))
    pathData = dict()
    pdiv = ":" + os.sep
    for propertie in splitData:
        propertie = propertie.replace(":\\","§pathDivider§")
        splitProp = propertie.split(':')
        prop_name = splitProp[0]
        prop_data = splitProp[1:len(splitProp)]
        prop_data = str(prop_data).replace("§pathDivider§",pdiv)
        prop_data = str(prop_data).replace("['","").replace("']","")
        prop_data = prop_data.replace(str(os.sep+os.sep),os.sep)
        # String
        if prop_data[0] == '"': pathData[prop_name] = str(prop_data).strip('"')
        # List
        if prop_data[0] == '[': pathData[prop_name] = str(prop_data).replace("[","").replace("]","").replace('"',"").split(',')
    #print("\033[31m" + str(pathData) + "\033[0m")
    return dict(pathData)

def cs_getPathablePath(pathables,inputs=str()):
    for cmdlet in pathables:
        cmdlet = cs_getPathableProperties(cmdlet)
        name = cmdlet["name"]
        aliases = cmdlet["aliases"]
        found = False
        if name.casefold() == inputs.casefold():
            found = True
        for alias in aliases:
            if inputs.casefold() == str(alias).casefold():
                found = True
        if found == True:
            path = cmdlet["path"]
            return path
    if found != True:
        return f"\033[31mError: Cmdlet '{inputs}' not found!\033[0m"

def cs_exec(path,params=list(),globalInput=None,captureOutput=False,PrintCmdletDebug=False):
    fending = str("." +''.join(path.split('.')[-1]))
    # Get file specific info
    if fending != ".exe":
        commentChar = "#"
        raw_content = open(path, 'r').read()
        headFound = False
        endFound = False
        configLines = []
        for line in raw_content.split('\n'):
            if f"{commentChar} [CStags]" in line:
                headFound = True
            if headFound == True:
                if f"{commentChar} [TagEnd]" in line:
                    endFound = True
                else:
                    configLines.append(line)
    else:
        configLines = ""
    # Hande config
    if "pwsh.passCSvars: True" in str(configLines):
        ps_retainVariables = True
    else:
        ps_retainVariables = False
    if "pwsh.returnCSVars: True" in str(configLines):
        ps_passBackVars = True
    else:
        ps_passBackVars = False
    if "pwsh.legacyNames: True" in str(configLines):
        ps_legacynames = True
    else:
        ps_legacynames = False
    if "pwsh.allowFuncCalls: True" in str(configLines):
        ps_allowFuncCalls = True
    else:
        ps_allowFuncCalls = False

    # [Accual execution]
    # Python
    if fending == ".py":
        globalInput["argv"] = params
        if captureOutput == True:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            if PrintCmdletDebug == True:
                exec(open(path).read(), globalInput)
            else:
                try:
                    exec(open(path).read(), globalInput)
                except:
                    print("\033[33mCmdlet didn't execute fully, might be an error in the cmdlet code!\033[0m")
            sys.stdout = old_stdout
            capturedOutput = redirected_output.getvalue()
        else:
            capturedOutput = False
            if PrintCmdletDebug == True:
                exec(open(path).read(), globalInput)
            else:
                try:
                    exec(open(path).read(), globalInput)
                except:
                    print("\033[33mCmdlet didn't execute fully, might be an error in the cmdlet code!\033[0m")
    # Powershell
    elif fending == ".ps1":
        newVars,capturedOutput = cse.Powershell(path, params, ps_retainVariables, globalInput, ps_passBackVars, ps_legacynames, ps_allowFuncCalls, captureOutput)
        for e in newVars:
            globals()[e] = newVars[e]
    # Cmd
    elif fending == ".cmd" or fending == ".bat":
        capturedOutput = cse.batCMD(path, params, captureOutput)
    # Executable (Win)
    elif fending == ".exe":
        capturedOutput = cse.winEXE(path, params, captureOutput)
    # Return capturedOutput
    if captureOutput == True:
        return capturedOutput

def cs_settings_json(mode=str(),settings_file=str(),settings=dict()):
    # Load
    if mode == "load":
        with open(settings_file) as json_file:
            data = json.load(json_file)
        return data
    # Set
    if mode == "set":
        with open(settings_file, "w") as outfile:
            json.dump(settings, outfile)

def cs_settings(mode=str(),settings_file=str(),settings=dict()):
    # Load
    if mode == "load":
        with open(settings_file, "r") as yamli_file:
            settings = yaml.safe_load(yamli_file)
        return settings
    # Set
    if mode == "set":
        with open(settings_file, "w") as outfile:
            yaml.dump(settings, outfile)

def cs_persistance_yaml(mode=str(),dictionary=dict(),yaml_file=str()):
    if mode == "get":
        with open(yaml_file, "r") as yamli_file:
            dictionary = yaml.safe_load(yamli_file)
        return dictionary
    if mode == "set":
        with open(yaml_file, "w") as outfile:
            yaml.dump(dictionary, outfile)

def cs_persistance(mode=str(),name=None,data_file=str(),content=None):
    # Get
    if mode == "get":
        dictionary = cs_persistance_yaml("get",dict(),data_file)
        return dictionary.get(str(name))
    # Set
    if mode == "set":
        dictionary = cs_persistance_yaml("get",dict(),data_file)
        dictionary[str(name)] = str(content)
        cs_persistance_yaml("set",dictionary,data_file)
    # Remove / Unregister
    if mode == "remove":
        dictionary = cs_persistance_yaml("get",dict(),data_file)
        dictionary.remove(str(name))
        cs_persistance_yaml("set",dictionary,data_file)

def cs_handleCommonParameters(cmd=str(),params=list()):
    if len(params) != 0:
        lastParam = str(params[-1])
        # Help
        if lastParam == "/help" or lastParam == "/?" or lastParam == "-?" or lastParam == "/h" or lastParam == "/Help" or lastParam == "/H":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "get-help"
        # Search
        if lastParam == "/search" or lastParam == "/Search":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "help"
        # Webi
        if lastParam == "/webi" or lastParam == "/Webi":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "webi"
        # Calc
        if lastParam == "/calc" or lastParam == "/Calc":
            params.pop(-1)
            params = [cmd,*params]
            cmd = "calc"
    return cmd,params