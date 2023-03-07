# Hide&Seek functions file. Author: Simon Kalmi Claesson
# This file is meant to be used by the main file and contain al functions that dosen't have to be in the main file.
# Al UI functions are also here
#

# ============================================[Imports]===========================================
import os
import yaml
import sys
import platform
try:
    from pynput import keyboard as pykeyb
except:
    os.system("python3 -m pip install pynput")
    from pynput import keyboard as pykeyb

# =======================[ConUtils functions, Author: Simon Kalmi Claesson]=======================
# Clear function to clear the console
def clear(supress=False):
    # If suppress eq True
    if supress == True:
        return ""
    # Get platform
    platformv = platform.system()
    # Linux using clear
    if platformv == "Linux":
        os.system("clear")
    # Mac using clear
    elif platformv == "Darwin":
        os.system(f"clear")
    # Windows using cls
    elif platformv == "Windows":
        os.system("CLS") # Apply console size with windows.cmd.cls
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"
    
# Pause function
def pause(string=None):
    if string != None: print(string)
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p ''")
    # Mac using resize
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        #os.system(f"resize -s {height} {width}")
    # Windows using PAUSE
    elif platformv == "Windows":
            os.system("PAUSE > nul") # Apply console size with windows.cmd.cls
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Dummy function
def dummy(): pass

# Function to clear the input buffer
def clear_buffer():
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()


# ===========================================[Function]===========================================

# Function to read a config-yaml file passed as filename and return dictionary of that yml
def readConfig(filename=str()) -> dict:
    with open(filename, "r") as yamli_file:
        dictionary = yaml.safe_load(yamli_file) # Safe loading
    return dictionary

# Function to write a dictionary passed as dictionary to a yaml file passed as filename
def writeConfig(filename=str(), dictionary=str()) -> None:
    with open(filename, "w") as outfile:
        yaml.dump(dictionary, outfile)

# Function to get the total player index based on attributes, how much attributes change aswell as default values if a player is missing an attribute
def GetTotIndex(player=dict(),attributeModifiers=dict(),missing_attribute_default=float()) -> float():
    # Check player type and set modifierType variable to be the correct keyname used in config
    if player["type"] == "hider": modifierType = "hider_modifier"
    if player["type"] == "seeker": modifierType = "seeker_modifier"
    # Get a list of keys in players attribute data
    attributes = list(player["attributes"].keys())
    # Get the total index by iterating over the attributes in the config
    totalIndex = 0
    for attribute in attributes:
        # If the attribute is not present on the player set the value to the default
        if (player["attributes"]).get(attribute) == None or (player["attributes"]).get(attribute) == "":
            playerAttributeValue = missing_attribute_default
        #Otherwise get attribute value from the player data and multiply it with the attribute's modifer value
        else:
            playerAttributeValue = float(player["attributes"][attribute])
        totalIndex += round(playerAttributeValue * float(attributeModifiers[attribute][modifierType]),1) # Round incase python float value assumption
    # Return total index
    return totalIndex

# Function to render a border based on the terminal size
def border() -> None:
    global g_borderChar, g_borderFormatting, g_configFile # Global imports
    # Save the current position of the write head
    print("\033[s", end="")
    # If borderformatting is not specified set it to reset
    if g_borderFormatting == None or g_borderFormatting == str():
        g_borderFormatting = "0m"
    # Get terminal size
    columns, rows = os.get_terminal_size()
    # Print the top and bottom lines of characters
    print(f"\033[1;1H\033[{g_borderFormatting}{g_borderChar*columns}")
    print(f"\033[{rows-1};0H\033[{g_borderFormatting}{g_borderChar*columns}")
    # Iterate over each row and and print "char      char"
    for i in range(rows):
        # prit first char then second
        print(f"\033[{i};0H\033[{g_borderFormatting}{g_borderChar}")
        print(f"\033[{i};{columns}H\033[{g_borderFormatting}{g_borderChar}")
    # Return the write head to the original position
    print("\033[u", end="")

# =======================================[Keyboard handling]=======================================
key_pressed_global = None
# Define what happens when someone presses a key
def on_press(key):
    global key_pressed_global # Global import (last key pressed)
    # Get either char or name of key pressed
    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = key.name
    key_pressed_global = key_pressed # Update last key pressed
# Define a keyboard listener taking allowedkeys that are the only ones to break the functio (and if not passed just accept any key)
def listen_for_key(allowedKeys=None):
    global key_pressed_global # Global import (last key pressed)
    # Start listener
    listener = pykeyb.Listener(on_press=on_press)
    listener.start()
    # Check for keys in a loop
    while True:
        if key_pressed_global is not None:
            # Get last key pressed
            key_pressed = key_pressed_global
            key_pressed_global = None
            # If in allowedkeys stop the listener and return the pressed key
            if allowedKeys is None or key_pressed in allowedKeys:
                listener.stop()
                clear_buffer() # Clear keyboard buffer to stop keys from showing up in input() statements later.
                return key_pressed


# ===================================[KeyboardException Handler]===================================
# Function to handle Keyboard Interupts
def HandleKeybExcept():
    global callback # Get the last run function (The callback variable will be set by each function as a referce to where the user was last)
    # Print menu
    clear()
    border()
    print("\033[10;40H\033[33mDo you want to exit?\033[0m")
    print(f"\033[11;40H[\033[35mY\033[0m] Yes exit")
    print(f"\033[12;40H[\033[35mN\033[0m] No continue")
    # Wait for key
    allowedKeys = ["n","y"]
    key_pressed = listen_for_key(allowedKeys)
    # Config menu if asked
    if key_pressed == "n":
        # Try running the callback if an error occure inform the user and close the app (Closing is the best solution since the code is a bit buggy with calling functions from inside a except statement)
        try: callback()
        except:
            clear()
            print("\033[31mSomething went wrong during keyboard exception handling, please restart the application!\033[0m")
            exit()
    elif key_pressed == "y":
        clear()
        exit()

# [UI Functions]
# Function to show the UI and handle the creation of a player
def addPlayer():
  try: # Try/Except to catch keyboardInterputs
    # Set last run
    global callback
    callback = addPlayer
    # Get the config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    players = [p for p in list(config["players"].keys())] # List of players in the games config
    playerString = " ".join(players)
    existing_atttributes = [p for p in list(config["attribute_modifiers"].keys())] # Al attributes that exist in the game's config
    existing_atttributes_string = " ".join(existing_atttributes)
    print(f'\033[9;40H\033[34mPlayers: \033[32m{playerString}\033[0m')
    print(f'\033[10;40H\033[34mAttributes: \033[32m{existing_atttributes_string}\033[0m')
    name = input("\033[12;40H\033[33mThe name of the player to add?\033[0m ")
    name = name.lower()
    # If playername is empty or already exist go back to the previous menu
    if name == "": handlePlayers()
    if name in players:
        pause(f"\033[13;40H\033[31mPlayer {name} already exists! (Press any key to continue...)")
        handlePlayers()
    # Otherwise add a player
    else:
        # Create keys in dictionarie if they dont exist
        if config["players"].get(name) == None: config["players"][name] = dict()
        if config["players"][name].get("attributes") == None: config["players"][name]["attributes"] = dict()
        # Ask the user for attributes to add
        print(f"\033[13;40H\033[33mAdd attributes to {name} (Write them as <attributeName>:<attributeValue>)")
        attributeRaw = "temporaryValue"
        while attributeRaw != "":
            try: # Try incase errors with wrong input
                # Show info and ask for attribute input
                currentAttributes = [p for p in list(config["players"][name]["attributes"].keys())] #Get a list of al attributes the player currently have
                currentAttributes_string = " ".join(currentAttributes)
                print(f'\033[11;40H\033[34mCurrent attributes: \033[32m{currentAttributes_string}\033[0m')
                attributeRaw = input("\033[14;40H\033[33mAttribute data:\033[0m \033[34m(Press enter to stop adding attributes) \033[35m")
                attributeRaw = attributeRaw.lower()
                # if empty break
                if attributeRaw == "": break
                # Get size
                columns, rows = os.get_terminal_size()
                print(f"\033[14;40H{' '*columns}") # clear line
                attributeName = ((attributeRaw.split(":")[0]).strip(" ")).lower()
                attributeData = (attributeRaw.split(":")[1]).strip(" ")
                # Apply attribute to the player
                config["players"][name]["attributes"][attributeName] = float(attributeData)
            except: pass
        # ask for type? and apply it if passed
        ptype = input(f"\033[15;40H\033[33mWhat type is {name}? (Just press enter to have type random when playing) ")
        ptype = ptype.lower()
        config["players"][name]["type"] = ptype
        # Save changes
        writeConfig(g_configFile,config)
        handlePlayers()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to remove a player
def removePlayer():
  try: # Try/Except to catch keyboardInterputs
    # Set last run
    global callback
    callback = removePlayer
    # Get the config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    players = [p for p in list(config["players"].keys())] # List of players in the games config
    playerString = " ".join(players)
    existing_atttributes = [p for p in list(config["attribute_modifiers"].keys())] # Al attributes that exist in the game's config
    existing_atttributes_string = " ".join(existing_atttributes)
    print(f'\033[9;40H\033[34mPlayers: \033[32m{playerString}\033[0m')
    name = input("\033[10;40H\033[33mThe name of the player to remove?\033[0m ")
    name = name.lower()
    # If playername is empty or does not exist go back to the previous menu
    if name not in players:
        pause(f"\033[11;40H\033[31mPlayer {name} dosen't exist! (Press any key to continue...)")
        handlePlayers()
    # remove players
    else:
        config["players"].pop(name)
        # Save changes
        writeConfig(g_configFile,config)
        handlePlayers()
  except KeyboardInterrupt: HandleKeybExcept()

def modifyPlayer():
  try: # Try/Except to catch keyboardInterputs
    # Set last run
    global callback
    callback = modifyPlayer
    # Get size
    columns, rows = os.get_terminal_size()
    # Get the config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    players = [p for p in list(config["players"].keys())] # List of players in the games config
    playerString = " ".join(players)
    existing_atttributes = [p for p in list(config["attribute_modifiers"].keys())] # Al attributes that exist in the game's config
    existing_atttributes_string = " ".join(existing_atttributes)
    print(f'\033[9;40H\033[34mPlayers: \033[32m{playerString}\033[0m')
    print(f'\033[10;40H\033[34mAttributes: \033[32m{existing_atttributes_string}\033[0m')
    name = input("\033[12;40H\033[33mThe name of the player to Modify?\033[0m ")
    name = name.lower()
    # If playername is empty or does not exist go back to the previous menu
    if name not in players:
        pause(f"\033[13;40H\033[31mPlayer {name} dosen't exist! (Press any key to continue...)")
        handlePlayers()
    # Ask what to do to the players attributes
    else:
        # Create keys incase they are missing
        if config["players"].get(name) == None: config["players"][name] = dict()
        if config["players"][name].get("attributes") == None: config["players"][name]["attributes"] = dict()
        action = input(f"\033[13;40H\033[33mWhat to do to {name}'s attributes \033[0m([\033[35mR\033[0m] to remove, [\033[35mA\033[0m]: add, [\033[35mM\033[0m]: modify)")
        print(f"\033[13;40H{' '*columns}")
        # Add attribute
        if action.lower() == "a":
            print(f"\033[13;40H\033[33mAdd attributes to {name} (Write them as <attributeName>:<attributeValue>)")
            attributeRaw = "temporaryValue"
            # Ask the player for attributes
            while attributeRaw != "":
                try: # Try incase errors with wrong input
                    # Print attributes
                    stringBuild = '\033[11;40H\033[34mCurrent attributes: '
                    for atrb in list(config["players"][name]["attributes"].keys()):
                        stringBuild += f'\033[32m{atrb}: {config["players"][name]["attributes"][atrb]}, '
                    print((stringBuild.strip(" ")).strip(","))
                    # ask user
                    attributeRaw = input("\033[14;40H\033[33mAttribute data:\033[0m \033[34m(Press enter to stop adding attributes) \033[35m")
                    attributeRaw = attributeRaw.lower()
                    if attributeRaw == "": break
                    # Get size
                    columns, rows = os.get_terminal_size()
                    print(f"\033[14;40H{' '*columns}") # Clear question line
                    attributeName = ((attributeRaw.split(":")[0]).strip(" ")).lower()
                    attributeData = (attributeRaw.split(":")[1]).strip(" ")
                    # Apply changes
                    config["players"][name]["attributes"][attributeName] = float(attributeData)
                except: pass
        # remove attribute
        elif action.lower() == "r":
            print(f"\033[13;40H\033[33mRemove attributes from {name} (Write them as <attributeName>)")
            attributeRaw = "temporaryValue"
            # Ask the player for attributes
            while attributeRaw != "":
                try: # Try incase errors with wrong input
                    currentAttributes = [p for p in list(config["players"][name]["attributes"].keys())] # Get a list of the players attributes (current)
                    currentAttributes_string = " ".join(currentAttributes)
                    print(f'\033[11;40H\033[34mCurrent attributes: \033[32m{currentAttributes_string}\033[0m')
                    # ask user
                    attributeRaw = input("\033[14;40H\033[33mAttribute name:\033[0m \033[34m(Press enter to stop removing attributes) \033[35m")
                    attributeRaw = attributeRaw.lower()
                    if attributeRaw == "": break
                    # Get size
                    columns, rows = os.get_terminal_size()
                    print(f"\033[14;40H{' '*columns}") # Clear question line
                    attributeName = (attributeRaw).lower()
                    config["players"][name]["attributes"].pop(attributeName)
                    # Apply changes
                    print(f"\033[11;40H{' '*columns}")
                except: pass
        # Modify attribute
        elif action.lower() == "m":
            print(f"\033[13;40H\033[33mModify attributes of {name} (Write them as <attributeName>:<attributeValue>)")
            attributeRaw = "temporaryValue"
            # Ask the player for attributes
            while attributeRaw != "":
                try: # Try incase errors with wrong input
                    # Print attributes
                    stringBuild = '\033[11;40H\033[34mCurrent attributes: '
                    for atrb in list(config["players"][name]["attributes"].keys()):
                        stringBuild += f'\033[32m{atrb}: {config["players"][name]["attributes"][atrb]}, '
                    print((stringBuild.strip(" ")).strip(","))
                    # ask user
                    attributeRaw = input("\033[14;40H\033[33mAttribute data:\033[0m \033[34m(Press enter to stop modifying attributes) \033[35m")
                    attributeRaw = attributeRaw.lower()
                    if attributeRaw == "": break
                    # Get size
                    columns, rows = os.get_terminal_size()
                    print(f"\033[14;40H{' '*columns}") # Clear question line
                    attributeName = ((attributeRaw.split(":")[0]).strip(" ")).lower()
                    attributeData = (attributeRaw.split(":")[1]).strip(" ")
                    # Apply changes
                    config["players"][name]["attributes"][attributeName] = float(attributeData)
                except: pass
        # Save changes
        writeConfig(g_configFile,config)
        handlePlayers()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to show menu regarding the handling of players
def handlePlayers():
  try: # Try/Except to catch keyboardInterputs
    # Set lastrun
    global callback 
    callback = handlePlayers
    # Show menu
    clear()
    border()
    print("\033[10;40H\033[33mWhat do you want to do?\033[0m")
    print(f"\033[11;40H[\033[35mA\033[0m] Add players")
    print(f"\033[12;40H[\033[35mR\033[0m] Remove players")
    print(f"\033[13;40H[\033[35mM\033[0m] Modify players")
    print(f"\033[14;40H[\033[35mB\033[0m] Go back")
    # Wait for key
    allowedKeys = ["a","r","m","b"]
    key_pressed = listen_for_key(allowedKeys)
    # Run actions based on keys
    if key_pressed == "a":
        addPlayer()
    elif key_pressed == "r":
        removePlayer()
    elif key_pressed == "m":
        modifyPlayer()
    elif key_pressed == "b":
        showConfig()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to add an attribute
def addAttributes():
  try: # Try/Except to catch keyboardInterputs
    # Set lastrun
    global callback
    callback = addAttributes
    # Get config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    # Show al atributes and their modifiers that are pressent in the config
    stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
    for atrb in list(config["attribute_modifiers"].keys()):
        hider = config["attribute_modifiers"][atrb]["hider_modifier"]
        seeker = config["attribute_modifiers"][atrb]["seeker_modifier"]
        stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
    print(stringBuild)
    # Ask user for input in loop
    print(f"\033[13;40H\033[33mAdd attributes (Write them as <attributeName>:<hiderModifier>,<seekerModifier>)")
    attributeRaw = "temporaryValue"
    while attributeRaw != "":
        try: # Try incase errors with wrong input
            # Get input
            attributeRaw = input("\033[14;40H\033[33mAttribute data:\033[0m \033[34m(Press enter to stop creating attributes) \033[35m")
            attributeRaw = attributeRaw.lower()
            # If empty break
            if attributeRaw == "": break
            # Get size
            columns, rows = os.get_terminal_size()
            print(f"\033[14;40H{' '*columns}") # Clear line
            # parse input
            attributeName = ((attributeRaw.split(":")[0]).strip(" ")).lower()
            attribute_hiderMod = ((attributeRaw.split(":")[1]).strip(" ")).split(",")[0]
            attribute_seekerMod = ((attributeRaw.split(":")[1]).strip(" ")).split(",")[1]
            # create missing keys and apply changes
            if config["attribute_modifiers"].get(attributeName) == None: config["attribute_modifiers"][attributeName] = dict()
            config["attribute_modifiers"][attributeName]["hider_modifier"] = float(attribute_hiderMod)
            config["attribute_modifiers"][attributeName]["seeker_modifier"] = float(attribute_seekerMod)
            # Redraw menu to clean up, then print out current attributes in the config            
            clear()
            border()
            stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
            # print attributes
            for atrb in list(config["attribute_modifiers"].keys()):
                hider = config["attribute_modifiers"][atrb].get("hider_modifier")
                seeker = config["attribute_modifiers"][atrb].get("seeker_modifier")
                stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
            print(stringBuild)
            print(f"\033[13;40H\033[33mModify attributes (Write them as <attributeName>)")
        except: pass
    # Save changes
    writeConfig(g_configFile,config)
    handleAttributes()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to remove an attribute
def removeAttributes():
  try: # Try/Except to catch keyboardInterputs
    # Set lastrun
    global callback
    callback = modifyAttributes
    # Get config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
    # print out attributes that are in config
    for atrb in list(config["attribute_modifiers"].keys()):
        hider = config["attribute_modifiers"][atrb]["hider_modifier"]
        seeker = config["attribute_modifiers"][atrb]["seeker_modifier"]
        stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
    print(stringBuild)
    # Ask user for input
    print(f"\033[13;40H\033[33mRemove attributes (Write them as <attributeName>)")
    attributeRaw = "temporaryValue"
    while attributeRaw != "":
        try: # Try incase errors with wrong input
            attributeRaw = input("\033[14;40H\033[33mAttribute name:\033[0m \033[34m(Press enter to stop removing attributes) \033[35m")
            attributeRaw = attributeRaw.lower()
            # if empty break
            if attributeRaw == "": break
            # Get size
            columns, rows = os.get_terminal_size()
            print(f"\033[14;40H{' '*columns}") # clear line
            # apply changes (remove atrb)
            attributeName = attributeRaw.strip(" ")
            config["attribute_modifiers"].pop(attributeName)
            # Redraw to stay clean
            clear()
            border()
            stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
            # print current attribute (redraw)
            for atrb in list(config["attribute_modifiers"].keys()):
                hider = config["attribute_modifiers"][atrb].get("hider_modifier")
                seeker = config["attribute_modifiers"][atrb].get("seeker_modifier")
                stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
            print(stringBuild)
            print(f"\033[13;40H\033[33mModify attributes (Write them as <attributeName>)")
        except: pass
    # Save changes
    writeConfig(g_configFile,config)
    handleAttributes()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to modify an attributes values
def modifyAttributes():
  try: # Try/Except to catch keyboardInterputs
    # Set lastrun
    global callback
    callback = modifyAttributes
    # Get config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    border()
    stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
    # print attributes and their values for both seeker and hider
    for atrb in list(config["attribute_modifiers"].keys()):
        hider = config["attribute_modifiers"][atrb]["hider_modifier"]
        seeker = config["attribute_modifiers"][atrb]["seeker_modifier"]
        stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
    print(stringBuild)
    # ask input in loop
    print(f"\033[13;40H\033[33mModify attributes (Write them as <attributeName>)")
    attributeRaw = "temporaryValue"
    while attributeRaw != "":
        try: # Try incase errors with wrong input
            # Show info and ask for attribute input
            attributeRaw = input("\033[14;40H\033[33mAttribute name:\033[0m \033[34m(Press enter to stop modifying attributes) \033[35m")
            attributeRaw = attributeRaw.lower()
            if attributeRaw == "": break # if empty close
            columns, rows = os.get_terminal_size() # get size
            print(f"\033[14;40H{' '*columns}") # clear line
            attributeName = attributeRaw.strip(" ")
            # create keys if missing
            if config["attribute_modifiers"].get(attributeName) == None: config["attribute_modifiers"][attributeName] = dict()
            # ask for input regarding what to do with an attribute
            action = input(f"\033[14;40H\033[33mWhat do you want to do to {attributeName}? \033[0m([\033[35mH\033[0m] Change hiderMod, [\033[35mS\033[0m]: Change seekerMod)")
            # Change hider value if h was given as input
            if action.lower() == "h":
                print(f"\033[14;40H{' '*columns}") # clear question line
                # ask for input
                hiderVal = input(f"\033[14;40H\033[33Hider modifier for {attributeName}: ")
                hiderVal = hiderVal.lower()
                # apply input
                config["attribute_modifiers"][attributeName]["hider_modifier"] = float(hiderVal)
            # Change seeker value if s was given as input
            elif action.lower() == "s":
                print(f"\033[14;40H{' '*columns}") # clear question line
                # ask for input
                seekerVal = input(f"\033[14;40H\033[33Seeker modifier for {attributeName}: ")
                seekerVal = seekerVal.lower()
                # apply input
                config["attribute_modifiers"][attributeName]["seeker_modifier"] = float(seekerVal)
            # Redraw for cleenes and reprint attributes to update them
            clear()
            border()
            stringBuild = "\033[10;40H\033[32mAttributes: \033[0m\033[11;5H"
            # print attributes
            for atrb in list(config["attribute_modifiers"].keys()):
                hider = config["attribute_modifiers"][atrb].get("hider_modifier")
                seeker = config["attribute_modifiers"][atrb].get("seeker_modifier")
                stringBuild += f"\033[33m{atrb}\033[0m:(\033[34mH:\033[35m{hider}\033[34m,S:\033[35m{seeker}\033[0m) "
            print(stringBuild)
            print(f"\033[13;40H\033[33mModify attributes (Write them as <attributeName>)")
        except: pass
    # Save changes
    writeConfig(g_configFile,config)
    handleAttributes()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to show a menu asking how to handle attributes
def handleAttributes():
  try: # Try/Except to catch keyboardInterputs
    # set lastset
    global callback
    callback = handleAttributes
    # Show menu
    clear()
    border()
    print("\033[10;40H\033[33mWhat do you want to do?\033[0m")
    print(f"\033[11;40H[\033[35mA\033[0m] Add modifiers")
    print(f"\033[12;40H[\033[35mR\033[0m] Remove modifiers")
    print(f"\033[13;40H[\033[35mM\033[0m] Modify modifiers")
    print(f"\033[14;40H[\033[35mB\033[0m] Go back")
    # Wait for key
    allowedKeys = ["a","r","m","b"]
    key_pressed = listen_for_key(allowedKeys)
    # Run actions based on keys pressed
    if key_pressed == "a":
        addAttributes()
    elif key_pressed == "r":
        removeAttributes()
    elif key_pressed == "m":
        modifyAttributes()
    elif key_pressed == "b":
        showConfig()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to show a menu asking the user what to configure
def showConfig():
  try: # Try/Except to catch keyboardInterputs
    # set lastset
    global callback
    callback = handleAttributes
    # Show menu
    clear()
    border()
    print("\033[10;40H\033[33mWhat do you want to do?\033[0m")
    print(f"\033[11;40H[\033[35mP\033[0m] Players")
    print(f"\033[12;40H[\033[35mA\033[0m] Attributes")
    print(f"\033[13;40H[\033[35mB\033[0m] Go back")
    # Wait for key
    allowedKeys = ["p","a","b"]
    key_pressed = listen_for_key(allowedKeys)
    # call functions based on input
    if key_pressed == "p":
        handlePlayers()
    elif key_pressed == "a":
        handleAttributes()
    elif key_pressed == "b":
        showUI()
  except KeyboardInterrupt: HandleKeybExcept()

# Function to show a list of al data in the config (print out yaml equiv...)
def listData():
  try: # Try/Except to catch keyboardInterputs
    # set lastset
    global callback
    callback = handleAttributes
    # get config
    global g_configFile
    config = readConfig(g_configFile)
    # Show menu
    clear()
    print("\033[33m"+yaml.dump(config)+"\033[0m")
    # press any key to go back
    print("\033[32mPress any key to go back...\033[0m")
    pause()
    showUI()
  except KeyboardInterrupt: HandleKeybExcept()

# GLOBALS (Define global variables)
g_borderChar, g_borderFormatting, g_configFile = None,None,None
callback = dummy # dummy is a dummy function passed as default callback

# main ui function asking what the user wants to do, takes arguments if given and sets global variables accordingly
def showUI(args=None) -> None:
    # Set lastrun
    global callback
    callback = showUI
    # Show menu
    try: # Try/Except to catch keyboardInterputs
        # Get global variables
        global g_borderChar, g_borderFormatting, g_configFile
        # If no arguments passed are not None, then set global variables to correct values
        if args != None:
            g_borderChar, g_borderFormatting, g_configFile = args["borderChar"], args["borderFormatting"], args["configFile"]
        # Show menu asking what to do
        clear()
        border()
        print("\033[10;40H\033[33mWhat do you want to do?\033[0m")
        print(f"\033[11;40H[\033[35mP\033[0m] Play")
        print(f"\033[12;40H[\033[35mL\033[0m] List data")
        print(f"\033[13;40H[\033[35mC\033[0m] Configure")
        print(f"\033[14;40H[\033[35mE\033[0m] Exit")
        # Wait for key
        allowedKeys = ["p","c","e","l"]
        key_pressed = listen_for_key(allowedKeys)
        # Config menu if asked
        if key_pressed == "c":
            showConfig()
        # List data if asked
        elif key_pressed == "l":
            listData()
        # exit if asked
        elif key_pressed == "e":
            clear()
            exit()
        # play if asked
        elif key_pressed == "p":
            print("\033[1;1H\033[0m.")
            clear()
    except KeyboardInterrupt: HandleKeybExcept()