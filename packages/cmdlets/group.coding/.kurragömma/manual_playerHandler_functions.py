# [Imports]
import yaml

# [Define playerhandler] Action: "add", "remove", "edit"
def playerhandlerUser(players=None,action=None) -> dict:
    # Players must be dict
    if players is not None and not isinstance(players, dict):
        raise TypeError("Argument 'players' must be a dictionary")
    # Get player amount
    playerAmount = len(players["hiders"] | players["seekers"])
    # If no players are set add players
    if playerAmount < 2: action = "add" # 2 since you must have a hider an one seeker
    # Add players
    if action == "add":
        print("To add players fillin player information, then press continue or add another one. (Note! You must have atleast one hider and one seeker")
        state_askforplayers = True
        while state_askforplayers:
            name = input("Name: ")
            state_askforattributes = True
            print(f"Please enter the attribute and the attribute-value to add to {name} (In the format of <name>:<value>)")
            attributes = {}
            # Add attributes (Loop to allow multiple additions)
            while state_askforattributes:
                # Some format handling
                attributeRaw = input("AttributeData: ")
                attributeName = attributeRaw.split(":")[0]
                attributeData = attributeRaw.split(":")[1]
                attributes = attributes | {attributeName: attributeData}
                # Add them?
                print(f"Current attributes: {', '.join([item for item in attributes])}")
                c = input("Press enter to continue with only the added attributes, or press + then enter to add another one")
                if c.lower() != "+":
                    state_askforattributes = False
            # Add attributes
            players = players | {name: attributes}
            # Add another player?
            print(f"Current players: {', '.join([player for player in players])}")
            c = input("Do you want to add another player? [y/n] ")
            if c.lower() != "y":
                state_askforplayers = False
    # Remove players
    elif action == "remove":
        print(f"Current players: {', '.join([player for player in players])}")
        state_askforplayers = True
        while state_askforplayers:
            name = input("Who do you want to remove? (Name): ")
            if name in players:
                players.pop(name)
                state_askforplayers = False
            else:
                print("\033[31mPlayer {name} does not exist!")
    # Edit players
    elif action == "edit":
        print(f"Current players: {', '.join([player for player in players])}")
        state_askforplayers = True
        # Players to edit (Loop)
        while state_askforplayers:
            name = input("Who do you want to edit? (Name): ")
            if name not in players:
                print("\033[31mPlayer {name} does not exist!")
            else:
                # Get attributes (current)
                attributes = players[name]
                print(f"Current attributes: {', '.join([item for item in players[name]])}")
                act = input(f"Do you want to remove or add attributes to {name}? [add/remove/modify] ")
                # Add more
                if act == "add":
                    state_askforattributes = True
                    print(f"Please enter the attribute and the attribute-value to add to {name} (In the format of <name>:<value>)")
                    while state_askforattributes:
                        # formatting
                        attributeRaw = input("AttributeData: ")
                        attributeName = attributeRaw.split(":")[0]
                        attributeData = attributeRaw.split(":")[1]
                        # add
                        attributes = attributes | {attributeName: attributeData}
                        # More?
                        print(f"Current attributes: {', '.join([item for item in attributes])}")
                        c = input("Press enter to continue with only the added attributes, or press + then enter to add another one")
                        if c.lower() != "+":
                            state_askforattributes = False
                # Remove attribute?
                elif act == "remove":
                    state_askforattributes = True
                    while state_askforattributes:
                        attributeToRemove = input("Attribute to remove: ")
                        # remove
                        if attributeToRemove in attributes:
                            attributes.pop(attributeToRemove)
                        else:
                            print(f"\033[31mAttribute {attributeToRemove} does not exist for {name}!\033[0m")
                        # more?
                        print(f"Current attributes: {', '.join([item for item in attributes])}")
                        c = input("Press enter to continue with only the current attributes, or press - then enter to remove another one")
                        if c.lower() != "-":
                            state_askforattributes = False
                # modify attributes?
                elif act == "modify":
                    state_askforattributes = True
                    while state_askforattributes:
                        print(f"Please enter the attribute and the attribute-value to add to {name} (In the format of <name>:<value>)")
                        attributeRaw = input("Attribute to change: ")
                        # formatting
                        attributeRaw = input("AttributeData: ")
                        attributeName = attributeRaw.split(":")[0]
                        attributeData = attributeRaw.split(":")[1]
                        # modify
                        if attributeName in attributes:
                            attributes[attributeName] = attributeData
                        else:
                            print(f"\033[31mAttribute {attributeToRemove} does not exist for {name}!\033[0m")
                        # more?
                        print(f"Current attributes: {', '.join([item for item in attributes])}")
                        c = input("Press enter to continue with the current attributes, or press + then enter to modify another one")
                        if c.lower() != "+":
                            state_askforattributes = False
                # Apply attribute changes
                players[name] = attributes
    # return finished dictionary
    return players
                
# Function to modify players by merging dictionaries
def playerhandler(players=dict(),playerData=dict(),action=str()) -> dict:
    '''
    Takes players dictionary containing al players then playerData is a players data {"<name>": <attributeDictionary>"}
    Action is either "add" or "remove" or "merge"
    '''
    key = list(playerData.keys())[0]
    if action == "add":
        players = players | playerData
    elif action == "remove":
        players.pop(key)
    elif action == "modify":
        players[key] = playerData[key]


                        
                    
                
