# Main functions for the zedix core
# Author: Simon Kalmi Claesson

# [Imports]
from assets.utils.utilFuncs import *
from assets.utils.conUtils import *
from assets.coreFuncs import *
from assets.lib.simpleDownload import simpleDownload
import assets.crossRunner as cse
import os
import sys
from io import StringIO
import yaml
import json
import traceback
import argparse

# Function to handle argumentParseErrors in argparse
class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()

# Functions to prep globals to send to cmdlets
def cs_prepGlobals(GlobalInput=dict(),varsToSendAdd=None,funcsToSendAdd=None):
    varsToSend = [
        # Crosshell
        "csbasedir",
        "cs_palette",
        "cspathables",
        "cs_cliargs",
        "cs_versionFile",
        "cs_settingsFile",
        "cs_persistanceFile",
        "csworking_directory",
        "allowedFileTypes",
        "path_packagesfolder",
        "path_cmdletsfolder",
        "path_cmdlet_zedix_core",
        "cssettings",
        "csversionData",
        "cs_prepGlobals",
        # Commands
        "pipeSTDOUT",
        "argv",
        "cmd",
        "params",
        # Palette Text
        "paletteText_standardPalette"
    ]
    funcsToSend = [
        # Crosshell
        "pt_format",
        "retbool",
        "cs_getPathablePath",
        "cs_execInput",
        "cs_writeProfile",
        "cs_writeWelcome",
        "saveTitle",
        "cs_getFending",
        # Crosshell ADV
        "cs_settings",
        "cs_exec",
        "cs_getPathablePath",
        "cs_getPathableProperties"
        # Utils
        "setConSize",
        "setConTitle",
        "clear",
        "pause",
        "boo",
        "dummy",
        "IsWindows",
        "IsLinux",
        "IsMacOS",
        "formatPrefix",
        # UtilFunctions
        "testPath",
        "getContent",
        "outFile",
        "touchFile",
        "scantree",
        "IsExecutable",
        "readConfig"
    ]
    varsToSend.update(*varsToSendAdd)
    funcsToSend.update(*funcsToSendAdd)
    newDict = {}
    try:
        for var in varsToSend: newDict[var] = GlobalInput[var]
    except: pass
    try:
        for func in funcsToSend: newDict[func] = GlobalInput[func]
    except: pass
    return newDict

# Function to get file endings
def cs_getFending(filepath):
    filename = os.path.basename(filepath)
    try:
        fending = str("." +''.join(filepath.split('.')[-1]))
        if IsLinux() or IsMacOS():
            if str(''.join(filepath.split('.')[-1])) != "." and str(os.sep) in fending and filename in str(fending.split(os.sep)[-1]) and IsExecutable(filepath):
                fending = "platform-binary"
    except:
        fending = ""
    return fending

# Function to load cmdlets
def cs_loadCmdlets(Path=str(),allowedFileTypes=list()):
    pathables = []
    if allowedFileTypes == []:
        allowedFileTypes = [".py"]
    entries = scantree(Path)
    for file in entries:
        fending = cs_getFending(file.path)
        valid = True
        completePath = os.path.realpath(str(file.path))
        cmdletPath = completePath.replace(Path,"")
        cmdletPath = cmdletPath.strip(os.sep)
        for elem in cmdletPath.split(os.sep):
            if str(elem) != "":
                if str(elem)[0] == ".":
                    valid = False
        if not ".cfg" in fending and file.name[0] != "." and fending in allowedFileTypes and os.path.isfile(file.path) == True and valid == True:
            # Handle path
            fpath = file.path
            fpath = fpath.replace('/',os.sep).replace('\\',os.sep)
            # Handle name
            fname = file.name
            if "." in fname:
                fname = fname.replace(fname.split('.')[-1],"").strip('.')
            # Handle other properties
            if fending != "platform-binary":
                fconfigfile =  fpath.replace(fending,".cfg")
            else:
                fconfigfile = fpath + ".cfg"
            faliases = "[]"
            # Non configfile defaults
            faliases = []
            fdescription = ""
            fparamhelp = ""
            fblockCommonparams = ""
            fsynopsisDesc = ""
            fargparseHelp = ""
            if os.path.exists(fconfigfile):
                fconfig = readConfig(fconfigfile)
                # config
                if fconfig.get("pathoverwrite") != "" and fconfig.get("pathoverwrite") != '""':
                    fpath = fconfig.get("pathoverwrite")
                    fpath = fpath.replace("{cmdletsFolder}",Path)
                    fpath = fpath.replace("\\",os.sep)
                    fpath = fpath.strip('"')
                    # F(ile)eding
                    fending = cs_getFending(fpath)
                if fconfig.get("nameoverwrite") != "" and fconfig.get("nameoverwrite") != '""':
                    fname = fconfig.get("nameoverwrite")
                    fname = fname.strip('"')
                if fconfig.get("aliases") != "" and fconfig.get("aliases") != '[]':
                    faliases = fconfig.get("aliases")
                if fconfig.get("description") != "" and fconfig.get("description") != '""':
                    fdescription = fconfig.get("description")
                    fdescription = str(fdescription).strip('"')
                if fconfig.get("paramhelp") != "" and fconfig.get("paramhelp") != '""':
                    fparamhelp = fconfig.get("paramhelp")
                    fparamhelp = str(fparamhelp).strip('"')
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
                if fconfig.get("ArgparseHelp") != "" and fconfig.get("ArgparseHelp") != '""':
                    fargparseHelp = fconfig.get("ArgparseHelp")
            # Add to pathables
            pathables.append(f'name%c%"{fname}"%sc%path%c%"{fpath}"%sc%aliases%c%{faliases}%sc%description%c%"{fdescription}"%sc%paramhelp%c%"{fparamhelp}"%sc%blockCommonParameters%c%"{fblockCommonparams}"%sc%synopsisDesc%c%{fsynopsisDesc}%sc%fileEnding%c%"{fending}"%sc%ArgparseHelp%c%"{fargparseHelp}"')
            fname,fpath,faliases,fdescription,fparamhelp = str(),str(),str('[]'),str(),str()
    return pathables

# Function to get properties of a pathable
def cs_getPathableProperties(pathData=str()):
    splitData = list(pathData.split('%sc%'))
    pathData = dict()
    #pdiv = ":" + os.sep
    for propertie in splitData:
        #propertie = propertie.replace("https://","§url_https_dividerr§")
        #propertie = propertie.replace("http://","§url_http_dividerr§")
        #propertie = propertie.replace(":\\","§pathDivider§")
        splitProp = propertie.split('%c%')
        prop_name = splitProp[0]
        prop_data = splitProp[1:]
        prop_data = '%c%'.join(splitProp[1:])
        prop_data = prop_data.strip("%c%")
        #prop_data = str(prop_data).replace("§pathDivider§",pdiv)
        #prop_data = str(prop_data).replace("§url_https_dividerr§","https://")
        #prop_data = str(prop_data).replace("§url_http_dividerr§","http://")
        prop_data = str(prop_data).replace("['","").replace("']","")
        prop_data = prop_data.replace(str(os.sep+os.sep),os.sep)
        try:
            # String
            if prop_data[0] == '"': pathData[prop_name] = str(prop_data).strip('"')
            # List
            if prop_data[0] == '[': pathData[prop_name] = str(prop_data).replace("[","").replace("]","").replace('"',"").split(',')
        except: pass
    #print("\033[31m" + str(pathData) + "\033[0m")
    return dict(pathData)

# Function to get pathable path
def cs_getPathablePath(pathables,inputs=str()):
    found = False
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
            if not os.path.exists(path):
                return f"\033[31mError: Path of cmdlet '{inputs}' not found!\033[0m"
            return path
    if found != True:
        return f"\033[31mError: Cmdlet '{inputs}' not found!\033[0m"

# Funtion to execute cmdlet
def cs_exec(path,params=list(),globalInput=None,captureOutput=False,HandleCmdletError=False,PrintCmdletDebug=False):
    # F(ile)eding
    fending = cs_getFending(path)
    # CSScriptRoot
    CSScriptRoot = (f'{os.sep}'.join((path.split(os.sep))[:-1])).strip(os.sep)
    if IsWindows() != True and CSScriptRoot[0] != "/":
        CSScriptRoot = "/" + CSScriptRoot
    globalInput["CSScriptRoot"] = CSScriptRoot
    # Get file specific info
    if fending != ".exe" and fending != "platform-binary":
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
        cmdlet = globalInput["cmd"]
        # If capture out is true, redirect stdout
        if captureOutput == True:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
        # Execute script
        if HandleCmdletError == True:
            try:
                exec(open(path).read(), globalInput)
            except Exception:
                if PrintCmdletDebug == True:
                    print(f"\033[31m{ traceback.format_exc() }\033[0m")
                else:
                    print(f"\033[33mCmdlet '{cmdlet}' didn't execute fully, might be an error in the cmdlet code!\033[0m")
            # Exit catcher (currently just passing along)
            except SystemExit as cs_cmdlet_exitcode:
                if str(cs_cmdlet_exitcode) == "cs.exit": exit()
                else: pass
        else:
            try:
                exec(open(path).read(), globalInput)
            # Exit catcher (currently just passing along)
            except SystemExit as cs_cmdlet_exitcode:
                if str(cs_cmdlet_exitcode) == "cs.exit": exit()
                else: pass
        # If capture output is true, restore stdout settings and save the captured output
        if captureOutput == True:
            sys.stdout = old_stdout
            capturedOutput = redirected_output.getvalue()

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
        if IsWindows():
            capturedOutput = cse.winEXE(path, params, captureOutput)
    # Return capturedOutput
        else:
            print("\033[31mError: Can't run windows executable on non windows systems!\033[0m")
    # Platform Executable
    elif fending == "platform-binary":
        if IsLinux() or IsMacOS():
            capturedOutput = cse.platformExe(path, params, captureOutput)
    # Return capturedOutput
        else:
            print("\033[31mError: Can't run non windows executable on windows systems!\033[0m")
    # Fallback
    else:
        print(f"\033[31mError: File ending/type '{fending}' is not supported by this crosshell version!\033[0m")
    if captureOutput == True:
        return capturedOutput

# Function to handle settings json
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

# Function to handle settings
def cs_settings(mode=str(),settings_file=str(),settings=dict()):
    # Load
    if mode == "load":
        with open(settings_file, "r") as yamli_file:
            settings = yaml.safe_load(yamli_file)
        preset = {"General":{"AutoClearConsole":"false","Prefix_Dir_Enabled":"true","Prefix_Enabled":"true","HandleCmdletError":"true","PrintCmdletDebug":"false","PrintComments":"false"},"SmartInput":{"Enabled":"true","EnhancedStyling":"true","TabCompletion":"true","History":"true","HistoryType":"Memory","HistorySuggest":"true","Highlight":"false","ShowToolBar":"true","MultiLine":"false","MouseSupport":"false","LineWrap":"true","CursorChar":"BLINKING_BEAM"},"Presets":{"Prefix":"> ","Title":"Crosshell (Zedix)"},"PaletteText_Palette":{}}
        try:
            v = settings
            if settings == "" or settings == {} or settings == None:
                try:
                    simpleDownload("https://github.com/simonkalmiclaesson/crosshell_zedix/raw/main/settings.yaml",settings_file)
                    with open(settings_file, "r") as yamli_file:
                        settings = yaml.safe_load(yamli_file)
                        v = settings
                except:
                    v = preset
        except:
            v = preset
        if v == preset:
            with open(settings_file, "w") as outfile:
                yaml.dump(v, outfile)
        return v
    # Set
    if mode == "set":
        with open(settings_file, "w") as outfile:
            yaml.dump(settings, outfile)

# Function to handle persistance yaml
def cs_persistance_yaml(mode=str(),dictionary=dict(),yaml_file=str()):
    if mode == "get":
        with open(yaml_file, "r") as yamli_file:
            dictionary = yaml.safe_load(yamli_file)
            if dictionary == "" or dictionary == {} or dictionary == None:
                dictionary = {}
        return dictionary
    if mode == "set":
        with open(yaml_file, "w") as outfile:
            yaml.dump(dictionary, outfile)

# Function to handle persistance
def cs_persistance(mode=str(),name=None,data_file=str(),content=None):
    # Get
    if mode == "get":
        dictionary = cs_persistance_yaml("get",dict(),data_file)
        try:
            v = dictionary.get(str(name))
        except:
            v = ""
        if v == None: return ""
        else: return str(v)
        
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

# Function to check if a string value is boolean true or false
def retbool(value):
    if value == "true" or value == "True" or value == True:
        return True
    else:
        return False