import os
fullMode = False
try:
    dirIn = str(argv[0])
    if "-a" in dirIn:
        dirIn = dirIn.replace("-a","")
        dirIn = dirIn.strip(" ")
        fullMode = True
    if dirIn != "":
        if os.path.exists(dirIn) == True:
            direc = dirIn
        else:
            print(f"\033[31mError: Directory '{dirIn}' couldn't be found!\033[0m")
            direc = os.getcwd()
    else: direc = os.getcwd()
except:
    direc = os.getcwd()

items = ""

try:
    items = os.scandir(os.path.realpath(direc))
except:
    print(f"\033[31mError: Directory '{dirIn}' couldn't not be listed.\033[0m")

if items != "" and items != None:
    string = ""
    for item in items:
        valid = True
        if fullMode != True:
            if str(item.name)[0] == ".":
                valid = False
        if valid:
            if item.is_dir():
                string += pt_format(cs_palette,f"\033[34;1m{item.name}\033[0;22m  ")
            else:
                fending = str("." +''.join(item.path.split('.')[-1]))
                if fending == ".py":
                    string += pt_format(cs_palette,f"\033[32m{item.name}\033[0m  ")
                elif fending == ".yaml" or fending == ".yml":
                    string += pt_format(cs_palette,f"\033[33m{item.name}\033[0m  ")
                elif fending == ".tmp":
                    string += pt_format(cs_palette,f"\033[90m{item.name}\033[0m  ")
                else:
                    string += pt_format(cs_palette,f"{item.name}  ")
    string.strip(" ")
    print(string)