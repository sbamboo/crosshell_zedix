# Shell information cmdlet
import os
from assets.lib.configlib import useYaml
from assets.lib.conUtils import IsLinux,IsMacOS,IsWindows

# [Variables]
version_file = f"{csbasedir}{os.sep}assets{os.sep}version.yaml"
lpt_file = f"{csbasedir}{os.sep}packages{os.sep}cmdlets{os.sep}crosshell.legacyPassThru.latest{os.sep}dir.cfg"
if IsWindows() == True: platformName = "Windows"
elif IsLinux() == True: platformName = "Linux"
elif IsMacOS() == True: platformName = "MacOS"
else:           platformName = "Unknown"
current_prefix = str(cs_persistance("get","cs_prefix",cs_persistanceFile))

# [Functions]
def ScrapeVersionData(coreFile=str()):
    content = open(coreFile,'r',encoding="utf-8").read()
    tmp = content.split("crosshell_versionID")[1]
    tmp = tmp.split("\n")[0]
    tmp = tmp.replace(" ","")
    tmp = tmp.replace("=","")
    tmp = tmp.replace('"',"")
    versionID = tmp.replace("'","")
    tmp = content.split("crosshell_versionChannel")[1]
    tmp = tmp.split("\n")[0]
    tmp = tmp.replace(" ","")
    tmp = tmp.replace("=","")
    tmp = tmp.replace('"',"")
    versionChannel = tmp.replace("'","")
    return {"VersionID":versionID,"VersionChannel":versionChannel}

# [Get raw data]
if os.path.exists(version_file):
    raw_data = useYaml(mode="get", yamlFile=version_file)
else: raw_data = {}

# [Verdata Scrape]
if os.path.exists(lpt_file):
    lpt_path = "Nan"
    try:
        path = open(lpt_file,'r',encoding="utf-8").read()
        if os.path.exists(path):
            lpt_path = path
    except: pass
else: lpt_path = "Nan"
if os.path.exists(f"{lpt_path}{os.sep}core{os.sep}core.ps1"):
    verData = ScrapeVersionData(f"{lpt_path}{os.sep}core{os.sep}core.ps1")
else: verData = {"VersionID":"Nan","VersionChannel":"Nan"}

# [Get Persistance]
cspersistance = useYaml(mode="get", yamlFile=cs_persistanceFile)

# [Get prefixes]
msgProfileFile = os.path.realpath(f"{csbasedir}{os.sep}assets{os.sep}profile.msg")
pyProfileFile = os.path.realpath(f"{csbasedir}{os.sep}assets{os.sep}profile.py")
if os.path.exists(pyProfileFile): prof_content = open(pyProfileFile,'r').read()
else: prof_content = open(msgProfileFile,'r').read()
pref = str(cs_persistance("get","cs_prefix",cs_persistanceFile))

# Get commands
cmdlets = []
for pathable in cspathables:
    data = cs_getPathableProperties(pathable)
    cmdlets.append(data["name"])

# [Data retrive]
if "noansi" in ' '.join(argv) or cs_cliargs.stripansi == True:
    headerFormat = ""
    labelFormat = ""
    sublabelFormat = ""
    valueFormat = ""
    resetFormat = ""
else:
    headerFormat = "\033[36m"
    labelFormat = "\033[33m"
    sublabelFormat = "\033[35m"
    valueFormat = "\033[32m"
    resetFormat = "\033[0m"
InfoBlock = pt_format(cs_palette,f'''
\033[97;44mShellinf cmdlet by Simon Kalmi Claesson, Version 1.0\033[0m

{headerFormat}VersionInfo:
  {labelFormat}Name:    {valueFormat}{raw_data.get("name")}
  {labelFormat}ID:      {valueFormat}{raw_data.get("id")}
  {labelFormat}Vid:     {valueFormat}{raw_data.get("vid")}
  {labelFormat}Channel: {valueFormat}{raw_data.get("channel")}

{headerFormat}Console:
  {labelFormat}Basedir: {valueFormat}{csbasedir}

{headerFormat}PlatformInfo:
  {labelFormat}Platform: {valueFormat}{platformName}

{headerFormat}Arguments:
  {labelFormat}Command:        {valueFormat}{str(cs_cliargs.command)}
  {labelFormat}FastCommand:    {valueFormat}{str(cs_cliargs.fastcommand)}
  {labelFormat}Action:         {valueFormat}{str(cs_cliargs.action)}
  {labelFormat}StartDir:       {valueFormat}{str(cs_cliargs.cli_startdir)}
  {labelFormat}StartPrefix:    {valueFormat}{str(cs_cliargs.cli_startprefix)}
  {labelFormat}NoExit:         {valueFormat}{str(cs_cliargs.noexit)}
  {labelFormat}NoCls:          {valueFormat}{str(cs_cliargs.nocls)}
  {labelFormat}NoWelcome:      {valueFormat}{str(cs_cliargs.nowelcome)}
  {labelFormat}NoInfo:         {valueFormat}{str(cs_cliargs.noinfo)}
  {labelFormat}StripANSI:      {valueFormat}{str(cs_cliargs.stripansi)}
  {labelFormat}Debug_Args:     {valueFormat}{str(cs_cliargs.debug_args)}
  {labelFormat}Debug_LoadOnly: {valueFormat}{str(cs_cliargs.debug_loadonly)}

{headerFormat}Settings:
  {labelFormat}General:
    {sublabelFormat}AllowRestart:       {valueFormat}{str(cssettings["General"]["AllowRestart"])}
    {sublabelFormat}AutoClearConsole:   {valueFormat}{str(cssettings["General"]["AutoClearConsole"])}
    {sublabelFormat}Prefix_Dir_Enabled: {valueFormat}{str(cssettings["General"]["Prefix_Dir_Enabled"])}
    {sublabelFormat}Prefix_Enabled:     {valueFormat}{str(cssettings["General"]["Prefix_Enabled"])}
    {sublabelFormat}HandleCmdletError:  {valueFormat}{str(cssettings["General"]["HandleCmdletError"])}
    {sublabelFormat}PrintCmdletDebug:   {valueFormat}{str(cssettings["General"]["PrintCmdletDebug"])}
    {sublabelFormat}PrintComments:      {valueFormat}{str(cssettings["General"]["PrintComments"])}
    {sublabelFormat}DefaultEncoding:    {valueFormat}{str(cssettings["General"]["DefaultEncoding"])}
  {labelFormat}SmartInput:           
    {sublabelFormat}Enabled:            {valueFormat}{str(cssettings["SmartInput"]["Enabled"])}
    {sublabelFormat}EnhancedStyling:    {valueFormat}{str(cssettings["SmartInput"]["EnhancedStyling"])}
    {sublabelFormat}TabCompletion:      {valueFormat}{str(cssettings["SmartInput"]["TabCompletion"])}
    {sublabelFormat}History:            {valueFormat}{str(cssettings["SmartInput"]["History"])}
    {sublabelFormat}HistoryType:        {valueFormat}{str(cssettings["SmartInput"]["HistoryType"])}
    {sublabelFormat}HistorySuggest:     {valueFormat}{str(cssettings["SmartInput"]["HistorySuggest"])}
    {sublabelFormat}Highlight:          {valueFormat}{str(cssettings["SmartInput"]["Highlight"])}
    {sublabelFormat}ShowToolBar:        {valueFormat}{str(cssettings["SmartInput"]["ShowToolBar"])}
    {sublabelFormat}MultiLine:          {valueFormat}{str(cssettings["SmartInput"]["MultiLine"])}
    {sublabelFormat}MouseSupport:       {valueFormat}{str(cssettings["SmartInput"]["MouseSupport"])}
    {sublabelFormat}LineWrap:           {valueFormat}{str(cssettings["SmartInput"]["LineWrap"])}
    {sublabelFormat}CursorChar:         {valueFormat}{str(cssettings["SmartInput"]["CursorChar"])}
  {labelFormat}Presets:
    {sublabelFormat}Prefix:             {valueFormat}{str(cssettings["Presets"]["Prefix"])}
    {sublabelFormat}Title:              {valueFormat}{str(cssettings["Presets"]["Title"])}
  {labelFormat}PaletteText:
    {sublabelFormat}Palette: {valueFormat}{str(cssettings["PaletteText_Palette"])}

{headerFormat}Persistance:
  {labelFormat}cs_prefix: {valueFormat}{str(cspersistance["cs_prefix"])}
  {labelFormat}cs_title:  {valueFormat}{str(cspersistance["cs_title"])}

{headerFormat}Title:
  {sublabelFormat}Raw: {valueFormat}{str(cspersistance["cs_title"])}

{headerFormat}Prefix:
  {labelFormat}Current:  {valueFormat}'{pref}{valueFormat}'
  {labelFormat}Rendered: {valueFormat}'{formatPrefix(pref,False,True,csworking_directory,globals())}{valueFormat}'
  {labelFormat}Showdir:  {valueFormat}'{formatPrefix(pref,True,True,csworking_directory,globals())}{valueFormat}'

{headerFormat}Profile:
  {labelFormat}MsgProfileFile: {valueFormat}{msgProfileFile}
  {labelFormat}PyProfileFile:  {valueFormat}{pyProfileFile}
  {labelFormat}ProfileContent: {valueFormat}{prof_content}

{headerFormat}Packages: {valueFormat}UNABLE TO LOAD!

{headerFormat}Pathables: {valueFormat}"{((((str(cmdlets)).strip('[')).strip(']')).replace("', '",";")).strip("'")}"

{headerFormat}Legacy Passthrough:
  {labelFormat}Path:    {valueFormat}{lpt_path}
  {labelFormat}VerID:   {valueFormat}{verData["VersionID"]}
  {labelFormat}Channel: {valueFormat}{verData["VersionChannel"]}
''')

print(InfoBlock)