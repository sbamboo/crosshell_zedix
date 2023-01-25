try:
    opts = argv 
except:
    opts = []

shownums = False
searchTerm = ""
if len(opts) != 0:
    if "--shownumerals" in str(opts) or "--num" in str(opts):
        shownums = True
        for i,elem in enumerate(opts):
            opts[i] = str(opts[i]).replace("--shownumerals", "")
            opts[i] = str(opts[i]).replace("--num", "")
            if opts[i] == "":
                opts.pop(i)
    try:
        searchTerm = str(opts[0])
    except:
        searchTerm = ""

gottenData = []
for pathable in cspathables:
    gottenData.append(cs_getPathableProperties(pathable))

# Handle searchterm
if searchTerm != "":
    mode = "exact"
    if searchTerm[-1] == "*":
        mode = "start"
    if searchTerm[0] == "*":
        mode = "end"
    if searchTerm[0] == "*" and searchTerm[-1] == "*":
        mode = "any"
    searchTerm = searchTerm.replace("*", "")
    filteredData = []
    for cmdlet in gottenData:
        name = str(cmdlet["name"])
        match = False
        if mode == "exact":
            if name == searchTerm:
                match = True
        elif mode == "start":
            name2 = name.removeprefix(searchTerm)
            if name != name2:
                match = True
        elif mode == "end":
            print(name,mode,searchTerm)
            name2 = name.removesuffix(searchTerm)
            print(name2)
            if name != name2:
                match = True
        elif mode == "any":
            name2 = name.replace(searchTerm,"")
            if name != name2:
                match = True
        # mm
        if match == True:
            filteredData.append(cmdlet)
    gottenData = filteredData

longest = ""
for cmdlet in gottenData:
    currentLen = len(str(cmdlet["name"]))
    longestLen = len(longest)
    if currentLen > longestLen:
        longest = str(cmdlet["name"])

amntCmdlets = len(gottenData)

print("")
if searchTerm == "":
    print(pt_format(cs_palette,f"     \033[32mCommands in shell: \033[90m{amntCmdlets} command(s)\033[0m"))
else:
    print(pt_format(cs_palette,f"      \033[32mMatched Commands: \033[90m{amntCmdlets} command(s)\033[0m"))
print(pt_format(cs_palette,"\033[32m==========================================\033[0m"))

for index,cmdlet in enumerate(gottenData):
    name = cmdlet["name"]
    desc = cmdlet["description"]
    desc = desc.replace("\\'","'")
    alis = cmdlet["aliases"]
    name = name + " "*(len(longest)-len(str(name)))
    path = cmdlet["path"]
    fending = cmdlet["fileEnding"]
    numpref = ""
    if shownums == True:
        numstr = " "*(len(str(len(gottenData))) - len(str(int(index+1)))) + str(int(index+1))
        numpref = f" {numstr}  "
    fendingpref = ""
    if fending == ".ps1":
        fendingpref = "  (pwsh)"
    elif fending == ".py":
        fendingpref = "  (native)"
    elif fending == ".exe":
        fendingpref = "  (win)"
    elif fending == ".cmd" or fending == ".bat":
        fendingpref = "  (cmd)"
    elif fending == "platform-binary":
        fendingpref = "  (platform-binary)"
    if desc == "" and fendingpref != "":
        fendingpref = fendingpref.strip(" ")
    if str(alis) == "['']":
        print(pt_format(cs_palette,f"\033[90m{numpref}\033[34m{name}  \033[90m{desc}\033[3;22;90m{fendingpref}\033[0m"))
    else:
        alis = str(alis).strip("[").strip("]").replace("'",'"').replace(",",", ")
        print(pt_format(cs_palette,f"\033[90m{numpref}\033[34m{name}  \033[90m{desc}  \033[37m{alis}\033[3;22;90m{fendingpref}\033[0m"))

print(pt_format(cs_palette,"\n\033[32m(Use 'get-help <command>' for more info about that command, including the 'help' command.)\033[0m\n"))