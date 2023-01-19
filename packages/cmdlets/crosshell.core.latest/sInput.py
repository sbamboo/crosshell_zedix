# [Imports]
import argparse

# [Arguments]
cparser = argparse.ArgumentParser(prog="sInput",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
# Arguments
cparser.add_argument('--GetHistory', action='store_true', help="Get smart input history")
cparser.add_argument('--ClearHistory', action='store_true', help="Clear History")
# Options (Comsume al remaining arguments)
cparser.add_argument('options', nargs='*')
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()

# [Get history]
if argus.GetHistory == True:
    # FileHistory
    if sInput_historyType == "File" or sInput_historyType == "FILE":
        # Get history content
        if os.path.exists(sInput_history_location) == True:
            hisContent = getContent(sInput_history_location)
            if hisContent != "" and hisContent != None:
                # Parse content
                print(pt_format(cs_palette,"\033[94;4mSmartInput history\033[0m"))
                hisContent = hisContent.strip("\n")
                entries = hisContent.split("\n\n")
                for entry in entries:
                    time = entry.split("\n")[0]
                    time = (time.strip("#")).strip(" ")
                    command = entry.split("\n")[1]
                    command = (command.strip("+")).strip(" ")
                    # Print content
                    print(pt_format(cs_palette,f"\033[32m[{time}]    \033[95m{command}\033[0m"))
    # Memory History
    elif sInput_historyType == "Memory" or sInput_historyType == "MEMORY":
        # Get content
        entries = list(session.history.load_history_strings())
        if len(entries) > 0:
            # Print Content
            print(pt_format(cs_palette,"\033[94;4mSmartInput history\033[0m"))
            for entry in entries:
                print(pt_format(cs_palette,f"\033[95m{entry}\033[0m"))
    # No historyType
    else:
        print(pt_format(cs_palette,"\033[31mERROR: HistoryType is invalid!\033[0m"))


# [Get history]
elif argus.ClearHistory == True:
    # Notice user
    choice = input(pt_format(cs_palette,"\033[33mClearing the history will remove al stored history in the persistance history file, this action can't be undone. Continue? [Y/N] \033[0m"))
    if choice == "Y" or choice == "y":
        # Clear history
        outFile("",sInput_history_location,append=False)
    else:
        print(pt_format(cs_palette,"\033[31mOperation Canceled!\033[0m"))




# No Input given
else:
    print(pt_format(cs_palette,"\033[33mPlease supply options (use '-h' for help)!\033[0m"))