import os,sys,importlib.util

def fromPath(path):
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
