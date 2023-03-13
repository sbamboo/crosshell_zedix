# Main Hide&Seek file, Author: Simon Kalmi Claesson
# Takes arguments --fastplay or --p to skip menu
# Takes arguments --help or --h to show argument, help
# Takes arguments --nostat or --ns to now show player attribute values
#
# This code import al other code and renders the output
#

# ============================================[Imports]============================================
import os
import random
import sys
# Fix import if running in croshell
try:
    from tabledraw import drawTable
    from functions import *
except:
    from assets.lib.importa import fromPath
    _tabledraw = fromPath(f"{CSScriptRoot}{os.sep}tabledraw.py")
    _functions = fromPath(f"{CSScriptRoot}{os.sep}functions.py")
    # Import all functions from tabledraw
    for name in dir(_tabledraw):
        if callable(getattr(_tabledraw, name)):
            globals()[name] = getattr(_tabledraw, name)
    # Import all functions from the functions
    for name in dir(_functions):
        if callable(getattr(_functions, name)):
            globals()[name] = getattr(_functions, name)

# ===========================================[Arguments]===========================================
try: arguments = argv # Crosshell compatibility since crosshell sends arguments through 'argv' instead of 'sys.argv'
except: arguments = sys.argv
# Args
if "--p" in arguments or "--fastplay" in arguments: fastplay = True
else: fastplay = False
if "--nostat" in arguments or "--ns" in arguments: nostat = True
else: nostat = False
# Help
if "--h" in arguments or "--help" in arguments:
    print("Usage:")
    print("--fastplay/--p: Skips menu, just plays")
    print("--nostat/--ns: Won's show player attributes")
    exit()

# ===========================================[Functions]===========================================
# Function to handle player types
def HandlePlayerTypes() -> dict:
    global players # Global imports
    SeekerTimes = [value["type"] for key,value in players.items()].count("seeker") # Iterate through players and get their type to a list. Then count the amount of seekers
    # If no seekers set random player to seeker
    if SeekerTimes == 0:
        players[random.choice(list(players.keys()))]["type"] = "seeker" # Get a random player 'random.choice' of a list of players 'players.keys()'
    # Set al non seekers to hiders
    for player in players:
        if players[player]["type"] != "seeker":
            players[player]["type"] = "hider"
    # Return players dictionary
    return players

# Function to randomize values also handles offsetting from config and likewise
def randomiser(offset_min,offset_max,offset_type) -> float:
    global player # Global Import
    indexonly = [value["index"] for index,value in players.items()] # Get a list of al players indexes and no other data
    mini = min(indexonly)
    maxi = max(indexonly)
    random_index = random.uniform(float(mini),float(maxi)) # Use random.uniform to handle random floating point numbers
    # Apply offsets, addative if offset_type is + and subtractive if offset_type is -
    if offset_type == "+": random_index += random.randint(offset_min, offset_max)
    elif offset_type == "-": random_index -= random.randint(offset_min, offset_max)
    # Return a random index value
    return random_index

# =============================================[Setup]=============================================
# Crosshell compatibility
try: ScriptRoot = CSScriptRoot                  # Fix if running in crosshell since crosshell sends working directory with 'CSScriptRoot' Variable
except: ScriptRoot = os.path.dirname(__file__)  #
# Variables
configFile = ScriptRoot + os.sep + "config.yml"
config = readConfig(configFile) # Read the config yaml to dict

# ==============================================[Menu]=============================================
# Show menu
ui = {
    "borderChar": "#",
    "borderFormatting": "33m",
    "configFile": configFile,
    "readConfig": readConfig,
}
if not fastplay: showUI(ui) # If fastplay is not enabled show menu with correct arguments
config = readConfig(configFile) # Reload config if user changed it in configuration menus

# ==============================================[Code]=============================================
# Define some quice use variables
players = config["players"]
attributes = config["attribute_modifiers"]
missing_attribute_default = float(config["missing_attribute_default"])
randomiserParameters = config["randomiser_parameters"]
total_seekerFactor = config["seekerfactor_default"]

# Handle types of players
players = HandlePlayerTypes()

# Get playerIndexes using GetTotIndex
for player in players:
    players[player]["index"] = GetTotIndex(players[player],attributes,missing_attribute_default) # Needs players[player] to get correct iteratpr instance
    players[player]["index"] = round(players[player]["index"],1) # Round incase python float value assumption

# Add random numbers to players indexes using randomiser function
for player in players:
    players[player]["index"] += randomiser(randomiserParameters["offset_min"],randomiserParameters["offset_max"],randomiserParameters["offset_type"])
    players[player]["index"] = round(players[player]["index"],1) # Round incase python float value assumption

# Calculate total seeker factor by adding together al seekers indexes
for player in players:
    if players[player]["type"] == "seeker":
        total_seekerFactor += players[player]["index"]
        players[player]["time"] = "Seeker"

# Calculate finding time for players by multiplying their index with the seeker factor (only do this for hiders)
for player in players:
    if players[player]["type"] == "hider":
        players[player]["time"] = players[player]["index"] * total_seekerFactor
        players[player]["time"] = round(players[player]["time"],1) # Round incase python float value assumption

# Sort player dictionary based on their time, putting seeker at bottom and winner at top
tobesorted = dict()
excluded = dict()
# Exclude seekers and select hiders to be sorted
for player in players:
    if str(players[player]["time"]).lower() != "seeker":
        tobesorted[player] = players[player]
    else:
        excluded[player] = players[player]
# Sort citionary based on time and return to dictionary
tobesorted = dict(sorted(tobesorted.items(), key=lambda item: item[1]["time"], reverse=True)) # Sort tobesorted based on time, in a reversed manner
# Copy the sorted dictionary to overwrite the non sorted original
players = tobesorted.copy()
# Add back in excluded players
for player in excluded:
    players[player] = excluded[player]

# Find if seeker won by checking if anyone is under 0
times = [players[player]["time"] for player in players] # Get a list of al player times
# Check if anyone has a time bellow zero and if so set bool anyAboveZeros to true
anyAboveZeros = False
for _time in times:
    if _time != "Seeker" and float(_time) > 0: anyAboveZeros = True
# If there are no above-zeros
if anyAboveZeros == False:
    # Go through all players and any player set seeker to win and any hider to lost
    for player in players:
        if players[player]["type"].lower() == "seeker":
            players[player]["result"] = "won"
        else:
            players[player]["result"] = "lost"
# If anyone has a time more then zero set winner to top player (Post sort so player with highest time is at top)
else:
    winner = list(players.keys())[0] # Get top player
    # Set won to winner and lost to rest
    for player in players:
        if player == winner:
            players[player]["result"] = "won"
        else:
            players[player]["result"] = "lost"


# =================================[Prep dictionary to be printed]=================================
# Add columns to the dictionary that will be printed
table = dict()
table["Players"] = list()
table["Time"] = list()
table["Result"] = list()
table["Type"] = list()
if nostat == False: table[""] = list() # Only add divider if nostat is disabled
table["Index"] = list()
for attribute in attributes:
    if nostat == False: # Dont add attribute-columns if nostat is disabled
        table[attribute] = list() 
table["Result"] = list()
# Now add in values for each players to the table
for player in players:
    table["Players"].append(player)
    table["Type"].append(players[player]["type"])
    table["Time"].append(players[player]["time"])
    # Apply attributes
    for attribute in attributes:
        if nostat == False:
            # Try/Except incase empty values
            try:
                table[attribute].append(str(float(players[player]["attributes"][attribute]))) # Append a row containing the players attribute-value. (Cast to float incase of int and then cast to string)
            except:
                table[attribute].append("")
    # Append index and result
    table["Index"].append(players[player]["index"])
    table["Result"].append(players[player]["result"])


# ============================================[Draw Menu]==========================================
title = '''
    __  __    _        __         ___      _____                __
   / / / /   (_)  ____/ /  ___   ( _ )    / ___/  ___   ___    / /__
  / /_/ /   / /  / __  /  / _ \ / __ \/|  \__ \  / _ \ / _ \  / //_/
 / __  /   / /  / /_/ /  /  __// /_/  <  ___/ / /  __//  __/ / ,<
/_/ /_/   /_/   \__,_/   \___/ \____/\/ /____/  \___/ \___/ /_/|_|
'''
print(f"\033[34m{title}\033[0m")
# Draw dictionary using drawTable function
print("")
print("\033[32m  Players (Winner in yellow)\033[0m")
print("\033[32m     ↓   \033[0m")
drawTable(table) # Drawtable with table dictionary
print("")

# Update attributes based on result
newconfig = readConfig(configFile) # Re read config so only new values will be saved later
# Iterate through players and check their results
for player in players:
    # Get players attributes and values as list of dictionaries
    playerAttributes = dict()
    playerAttributes_list = [{key:value} for key,value in players[player]["attributes"].items()] # Key-value pairs in dictionaries from the items in the players attributes
    # Now convert the list of dictionaries to one dictionary with nested dictionaries
    for i in range(len(playerAttributes_list)):
        atr = list(playerAttributes_list[i].keys())[0] # Get first key since only one key should be present
        playerAttributes[atr] = playerAttributes_list[i][atr]
    # Now sort the player attributes based on their value (DO THIS TWISE TO NOT HAVE TO REVERSE IT OR USE WIERD INDEX VALUES) Use lambda to sort based on the nested dictionaries values
    playerAttributes = dict(sorted(playerAttributes.items(), key=lambda x: x[1]))
    playerAttributes_rev = dict(sorted(playerAttributes.items(), key=lambda x: x[1], reverse=True))
    # Now get keylists for the two sorted dictionaries
    keysr = list(playerAttributes_rev.keys())
    keys = list(playerAttributes.keys())
    # If player won raise their lowest values (FLATTEN)
    if players[player]["result"] == "won":
        # Take random attribute from three lowest values and highen them
        lowest = list()
        if len(playerAttributes) == 1:
            lowest.append({keys[0]:playerAttributes[keys[0]]})
        if len(playerAttributes) == 2:
            lowest.append({keys[0]:playerAttributes[keys[0]]})
            lowest.append({keys[1]:playerAttributes[keys[1]]})
        if len(playerAttributes) >= 3:
            lowest.append({keys[0]:playerAttributes[keys[0]]})
            lowest.append({keys[1]:playerAttributes[keys[1]]})
            lowest.append({keys[2]:playerAttributes[keys[2]]})
        # Now get a random value of the highest attributes found earlier
        randomValue = random.choice(lowest)
        # Get the the key of the randomValue
        key = list(randomValue.keys())[0]
        # Now get a random modififier from 0.5 two 1.0 to add to the attribute
        randomModifier = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        # apply new attribute value to config to later be viewed and newconfig to be saved
        config["players"][player]["attributes"][key] = round(randomValue[key] + randomModifier,1)    # Round incase python float value assumption
        newconfig["players"][player]["attributes"][key] = round(randomValue[key] + randomModifier,1) # Round incase python float value assumption
        # Print the change made
        print(f"\033[33mAdded \033[34m{randomModifier}\033[33m to \033[35m{player}'s \033[33m{key}\033[33m (\033[32m{randomValue[key]}\033[33m>>\033[32m{config['players'][player]['attributes'][key]}\033[33m)\033[0m")
    # If the player lost instead lower their heighest score
    elif players[player]["result"] == "lost":
        # Take random attribute from three highest values and lower them
        highest = list()
        # Append first three if avaliable but if only one or two is available apply just those
        # keysr[0] is the name of the first key
        if len(playerAttributes_rev) == 1:
            highest.append({keysr[0]:playerAttributes_rev[keysr[0]]})
        if len(playerAttributes_rev) == 2:
            highest.append({keysr[0]:playerAttributes_rev[keysr[0]]})
            highest.append({keysr[1]:playerAttributes_rev[keysr[1]]})
        if len(playerAttributes_rev) >= 3:
            highest.append({keysr[0]:playerAttributes_rev[keysr[0]]})
            highest.append({keysr[1]:playerAttributes_rev[keysr[1]]})
            highest.append({keysr[2]:playerAttributes_rev[keysr[2]]})
        # Now get a random value of the lowest attributes found earlier
        randomValue = random.choice(highest)
        # Get the the key of the randomValue
        key = list(randomValue.keys())[0]
        # Now get a random modififier from 0.5 two 1.0 to add to the attribute
        randomModifier = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        # apply new attribute value to config to later be viewed and newconfig to be saved
        config["players"][player]["attributes"][key] = round(randomValue[key] - randomModifier,1)    # Round incase python float value assumption
        newconfig["players"][player]["attributes"][key] = round(randomValue[key] - randomModifier,1) # Round incase python float value assumption
        # Print the change made
        print(f"\033[33mRemoved \033[34m{randomModifier}\033[33m from \033[35m{player}'s \033[33m{key}\033[33m (\033[31m{randomValue[key]}\033[33m>>\033[31m{config['players'][player]['attributes'][key]}\033[33m)\033[0m")


# ===========================================[Show Changes]========================================
if nostat == False: # Dont show the table if nostat is enabled
    # Add columns to the dictionary that will be printed
    table = dict()
    table["Players"] = list()
    table["Time"] = list()
    table["Result"] = list()
    table["Type"] = list()
    table[""] = list()
    table["Index"] = list()
    for attribute in attributes:
        table[attribute] = list()
    table["Result"] = list()
    # Now add in values for each players to the table
    for player in players:
        table["Players"].append(player)
        table["Type"].append(players[player]["type"])
        table["Time"].append(players[player]["time"])
        for attribute in attributes:
            # Try/Except incase empty values
            try:
                table[attribute].append(str(float(players[player]["attributes"][attribute]))) # Append a row containing the players attribute-value. (Cast to float incase of int and then cast to string)
            except:
                table[attribute].append("")
        # Append index and result
        table["Index"].append(players[player]["index"])
        table["Result"].append(players[player]["result"])
    # Print some text then render the table
    print("")
    print("\033[32m  New values:\033[0m")
    drawTable(table)

# Save changes from newconfig dictionary
writeConfig(configFile,newconfig)

# Pause
pause("\033[34mPress any key to exit...\033[0m")