from libs.libRSA import *
import platform,os,sys,json

# Define functions
def setConTitle(title): # From SimonKalmiClaesson's conUtils library
    platformv = platform.system()
    if platformv in ["Linux", "Darwin"]:
        sys.stdout.write(f"\x1b]2;{title}\x07")
    elif platformv == "Windows":
        os.system(f'title {title}')
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"
def Finput(stri):
    i = input(stri)
    if i.lower == "None" or i == "": i = "None"
    return i
def Binput(stri):
    i = input(stri)
    if i.lower == "None" or i == "": i = "None"
    elif i.lower == "y": i = "False"
    elif i.lower == "n": i = "True"
    return i

# Take input
setConTitle("[GamehubAPI] API-key Configurator (1.0_win64)")
print("Input parameters for API configuration bellow, for help see docs for the ScoreboardConnector")
managerFile = Finput('ManagerFile path, ["<path>" / "None"]: ')
storageType = Finput('StorageManager to use, (Depends on your managerFile): ')
ignoreManagerFormat = Finput('Do you want to ignore managerFile format? [y/n]: ')
apiKey = Finput('API-key (Depends on your storageManager): ')
encType = Finput('API-key Encryptiontype ["aes" / "legacy" / "None"]: ')
encKey = Finput('API-key EncryptionKey (Only if encType is not "None"): ')
_confFile = input('Done!, Now where should the data be saved ["<path>"]: ')

# GenerateKey
public_key = "<PUBLIC_KEY>"

# Package to json
_dict = {"managerFile":managerFile, "storageType":storageType, "ignoreManagerFormat":ignoreManagerFormat, "apiKey":apiKey, "encType":encType, "encKey":encKey}
_json = json.dumps(_dict)

# Encrypt string
_json_encrypted = encrypt_string(_json, public_key)

# Save to file
open(_confFile, 'w').write(_json_encrypted)