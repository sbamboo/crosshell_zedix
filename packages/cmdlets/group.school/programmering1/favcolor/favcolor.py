# Version: 1.0 (Made by: Simon Kalmi Claesson)

# [Imports]
import os
import json
import difflib

# [Declarations]
colorFile = f"{os.getcwd()}{os.sep}color.txt"
defaultEncoding = "utf-8"
reset = "\033" # Back slashes can't be included in f-string expressions, so I use a variable.

# [Arguments (Crosshell only)]
try: arguments = argv
except: arguments = ""
if argv and argv[0] == "--removeFile":
    try:
        if os.path.exists(colorFile): os.remove(colorFile)
    except: pass
    exit()


# region [Functions]

# Function to save data to file
def saveToFile(filepath=str(),data=dict()):
    # Convert to string format
    str_data = str(data)
    # Write to file
    f = open(filepath, "w", encoding=defaultEncoding)
    f.write(str_data)
    f.close()
    
# Function to load data from file
def readFromFile(filepath=str()):
    dictionary = {}
    if os.path.exists(filepath):
        # Read data
        try:
            f = open(filepath, "r", encoding=defaultEncoding)
            str_data = f.read()
            f.close()
        except:
            print("\033[31mApon reading file got error 'An error occured, check permissions!'\033[0m")
            exit()
        # Convert data to dictionary
        str_data = str_data.replace("'",'"')
        dictionary = json.loads(str_data)
    # Return dictionary (Note! Will be empty if no file was found)
    return dictionary

# Function to fuzzy match a string (This is be able to give suggestions for usernames)
def suggest_name(name=str(),data=dict()):
    suggestions = difflib.get_close_matches(name, data.keys(), n=1, cutoff=0.6)
    if suggestions:
        suggestion = suggestions[0]
        if suggestion != name:
            response = input(f"\033[33mJust asking, did you mean '{suggestion}' instead? [y/n] \033[0m")
            if response.lower() == "y":
                return suggestion
    return name

# Function to get the ansi code for a color
def getColor(colorname=str(),bright=False):
    colorname = colorname.lower()
    # Bright colors
    if bright == True: colors = {
        "black": "90",  # Black
        "red": "91",  # Red
        "green": "92",  # Green
        "yellow": "93",  # Yellow
        "blue": "94",  # Blue
        "magenta": "95",  # Magenta
        "cyan": "96",  # Cyan
        "white": "97",  # White
    }
    # Normal Colors
    else: colors = {
        "black": "30",  # Black
        "red": "31",  # Red
        "green": "32",  # Green
        "yellow": "33",  # Yellow
        "blue": "34",  # Blue
        "magenta": "35",  # Magenta
        "cyan": "36",  # Cyan
        "white": "37",  # White
    }
    # Return ansi
    ansi = colors.get(colorname)
    colorstring = ""
    if ansi != None:
        colorstring = f"{reset}[{ansi}m"
    return colorstring

# Function to handle exit in inputs
def cinput(string=str()):
    c = input(string)
    if c == "exit": exit()
    else: return c

# endregion


# [Main Code]

# Retrive data
colorData = readFromFile(colorFile)
# Get name
user_name = cinput("\033[33mWhat is your name? \033[0m")
user_name = user_name.lower()
user_name = suggest_name(user_name,colorData)

# If the user does not exists, ask the user to save the color and save it
if not colorData.get(user_name):
    if cinput(f"\033[36mHello {user_name.capitalize()}, I can't find the memory of your favorite color.\n\033[33mDo you want me to remember it? [y/n] \033[0m").lower() == "y":
        user_color = cinput("\033[33mWhat is your favorite color? \033[0m")
        colorData[user_name] = user_color
        saveToFile(colorFile,colorData)
        print(f"\033[32mThanks {user_name.capitalize()}, i will remember that your favorite color is {getColor(user_color)+user_color+reset+'[32m'}!\033[0m")
    else:
        print("\033[32mOkay, I wont ask.\033[0m")
# If the user exists remind the user of their color and ask if the app should change it. Also if the app should forget it.
else:
    user_color = colorData[user_name]
    print(f"\033[36mHello {user_name.capitalize()}, I remember that your favorite color is: {getColor(user_color)+user_color+reset+'[36m'}\033[0m")
    # Change color?
    if cinput("\033[33mDo you want to change what favorite color i remember? [y/n] \033[0m").lower() == "y":
        user_color = cinput("\033[33mWhats your new favorite color? \033[0m")
        colorData[user_name] = user_color
        saveToFile(colorFile,colorData)
        print(f"\033[36mThanks {user_name.capitalize()}, i will remember that your favorite color is {getColor(user_color)+user_color+reset+'[36m'}!\033[0m")
    # Remove color?
    elif cinput(f"\033[33mDo you want me to forget your favorite color? [y/n] \033[0m").lower() == "y":
        colorData.pop(user_name)
        saveToFile(colorFile,colorData)
        print("\033[36mI wonder what your favorite color was...\033[0m")
    else:
        print("\033[32mOkay, bye!\033[0m")