import argparse

cparser = argparse.ArgumentParser(prog="Help",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
# Options
cparser.add_argument('--shownumerals','--num', dest="shownumerals", action='store_true', help="Show numbers.")
cparser.add_argument('--matchaliases','--ma', dest="matchaliases", action='store_true', help="Match for aliases.")
# Searchterm (Comsume al remaining arguments)
cparser.add_argument('searchterm', nargs='*', help="The cmdlet/searchterm to match to.")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

shownums = argus.shownumerals
opts = argus.searchterm
try:
    searchTerm = opts[0]
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
        aliases = cmdlet["aliases"]
        match = False
        if mode == "exact":
            if name == searchTerm or searchTerm in aliases:
                match = True
        elif mode == "start":
            name2 = name.removeprefix(searchTerm)
            if name != name2:
                match = True
            else:
                if argus.matchaliases:
                    for alias in aliases:
                        alias2 = searchTerm + str(alias).removeprefix(searchTerm)
                        if alias2 == alias:
                            match = True
        elif mode == "end":
            name2 = name.removesuffix(searchTerm)
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

# Sort gottenData    (x is the pathable-dictionary in the list then sort by the name key in lowercase since gottenData is a list of dictionaries)
gottenData = sorted(gottenData, key=lambda x: (x["name"].lower()))

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