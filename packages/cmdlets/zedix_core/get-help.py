command = ' '.join(argv)
path = cs_getPathablePath(cspathables,command)
if "Error:" in path:
    print(path)
else:
    found = False
    for pathable in cspathables:
        data = cs_getPathableProperties(pathable)
        if path == data["path"]:
            found = data
    # Print data
    if found != False:
        name = found["name"]
        path = found["path"]
        aliases = found["aliases"]
        description = found["description"]
        blockCommonParameters = found["blockCommonParameters"]
        try:
            paramhelp = found["paramhelp"]
        except:
            paramhelp = ""
        aliases = str(aliases).strip("[").strip("]").replace("'",'"').replace(",",", ")
        print(f"\033[34m{name}: \033[32m{description}\033[0m")
        if blockCommonParameters != "True":
            paramhelp += " [<CommonParameters>]"
            paramhelp = paramhelp.lstrip(" ")
        if paramhelp != "" and paramhelp != None:
            print(f"\033[33m{paramhelp}\033[0m")
        print(f"\033[33mAliases: {aliases}\033[0m")
        print("\033[90mFor more info about CommonParameters write 'webi commonparameters'\033[0m")