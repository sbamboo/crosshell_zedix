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
        argparseHelp = found["ArgparseHelp"]
        fending = cmdlet["fileEnding"]
        # Argparse help
        if argparseHelp == True or argparseHelp == "True" and fending == ".py": 
            int_old_stdout = sys.stdout
            int_redirected_output = sys.stdout = StringIO()
            try:    exec(open(path).read(), {"argv":['--exhelp']})
            except  SystemExit as cs_cmdlet_exitcode: pass
            except: pass
            sys.stdout = int_old_stdout
            print( int_redirected_output.getvalue() )
        # Normal Help text
        else:
            description = description.replace("§colon§",":")
            description = description.replace("\\'","'")
            try:
                paramhelp = f"Params: {found['paramhelp']}"
            except:
                paramhelp = ""
            aliases = str(aliases).strip("[").strip("]").replace("'",'"').replace(",",", ")
            print(pt_format(cs_palette,f"\033[34m{name}: \033[32m{description}\033[0m"))
            if blockCommonParameters != "True":
                paramhelp += " [<CommonParameters>]"
                paramhelp = paramhelp.lstrip(" ")
            if paramhelp != "" and paramhelp != None:
                print(pt_format(cs_palette,f"\033[33m{paramhelp}\033[0m"))
            print(pt_format(cs_palette,f"\033[33mAliases: {aliases}\033[0m"))
        # Bottom text
        print(pt_format(cs_palette,"\033[90mFor more info about CommonParameters write 'webi commonparameters'\033[0m"))