import os,sys,importlib.util,platform,requests

def pause():
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p ''")
    # Mac using resize
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # Windows using PAUSE
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
            os.system("PAUSE > nul") # Apply console size with windows.cmd.cls
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

def has_connection(override_url=None):
    # If no url is given, default to google.
    if override_url == None or override_url == "":
        override_url = "https://google.com"
    # Check/Validate the connection, catch exeptions and return boolean
    try:
        req = requests.get(override_url)
        req.raise_for_status()
        return True
    except:
        return False

def fromPath(path):
    path = path.replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

try:
    parent = CSScriptRoot
    argu = argv
except:
    parent = os.path.dirname(__file__)
    argu = sys.argv[1:]

os.chdir(parent)

qu = fromPath(f"{parent}\\GamehubAPI\\quickuseAPI.py")
ga = fromPath(f"{parent}\\GamehubAPI\\gamehubAPI.py")

tos = ga.gamehub_getTOS(net=has_connection())

if not os.path.exists(f"{parent}\\apiExcepted.empty"):
    print(tos)
    print("\nPress any key to accept the TOS and agknowledge that you have read the TOS... (To reject please close the app)")
    pause()
    open(f"{parent}\\apiExcepted.empty",'w').write("1")

qu.gamehub_saveService_on(apiConfPath=f"{parent}\API.sconf",linkedFile=f"{parent}\score.ght",exitFile=f"{parent}\exit.empty",verbose=True,simpleScore=True)

# Debug
commands = ""
argu_s = ' '.join(argu)
if "--debug" in argu_s:
    commands += " --debug"
    argu_s = argu_s.replace("--debug","")
# Params
if "-params" in argu_s:
    argu_s = argu_s.replace("-params","")
    commands += argu_s

os.system(f"powershell {parent}\\snake.ps1{commands}")

qu.gamehub_saveService_off(exitFile=f"{parent}\exit.empty")

linkedFile=f"{parent}\score.ght"

if qu._linkFileExist(linkedFile):
    apiC = qu.getAPIConfig(f"{parent}\API.sconf")
    _path = os.path.dirname(linkedFile)
    _file = os.path.basename(linkedFile)
    qu.gamehub_singleSave_score(encType=apiC["encType"],manager=apiC["storageType"],apiKey=apiC["apiKey"],encKey=apiC["encKey"],managerFile=apiC["managerFile"],ignoreManFormat=apiC["ignoreManagerFormat"],tempFolder=_path ,fileName=_file)
