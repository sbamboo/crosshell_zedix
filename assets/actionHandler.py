def cs_RunActions(actions_string,basedir=None):
    if actions_string:
        actions_string = actions_string.replace(" ","")
        actions = actions_string.split(";")

        actions_list = ["list: Lists out actions.","CdBdir: Cd's to basedir. (Crosshell's install directory)"]

        # Run Actions
        for action in actions:
            # List
            if action.lower() == "list":
                print("\033[94mActions:\033[0m")
                for actions_list_item in actions_list:
                    print(actions_list_item)
                exit()
            # CdBasedir
            if action.lower() == "cdbdir":
                if basedir != None:
                    print( basedir )
                exit()

