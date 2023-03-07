Hide&Seek made by Simon Kalmi Claesson
Version: 1.0

! This version is a schoolproject and falls under the rules for schoolwork setup by NTIG/Academedia ! (Note fututure version may be under separate rules since I am the author)

The project includes multiple files:
  main.py:      This is the main file and contains the main code. (Should be the one to be executed)
  functions.py: This file contains functions needed for the main code. (Aswell as UI)
  tabledraw.py: This file contains one function being the tabledraw function, that draws a function from a dictionary.
  config.yml:   This file is the games config file, containing al values saved cross sessions. (Se info bellow)

As said main.py should be the file to be executed!

main.py can be sent afew commandline arguments:
'--help' or '--h' shows a help menu for commandline arguments
'--fastplay' or '--p' will skip the menu and start the game emiditely
'--nostat' or '--ns' will not show player attribute data on the play screen

There is also a config.yml file that contains al values saved across sessions aswell as some settings: (Players and attributes can be changed ingame aswell as in the file)
  attributes:
    Contains al attributes in the game, to add attributes write their name as an indented value and then 'hider_modifier' and 'seeker_modifier' with their values indented bellow that.
  missing_attribute_default:
    This is the default value used when a player is missing an attribute that exists in the config but is not defined on the player.
  players:
    Contains al players in the game, type indented bellow is an overwrite of 'hider' or 'seeker' used to force a player's type. Attributes contains that players attributes and have them and their values indented bellow it.
  randomiser_parameters:
    Contains defaults and options for the randomiser.
    offset_type:
        This is the way to offset the random value generated to determine player index. can be '' to turn off or '+' to be addative or '-' to be subtractive
    offset_max:  
        This is the max value to randomise an offset from
    offset_min:
        This is the min value to randomise an offset from
  seekerfactor_default:
    This is the default value for when no seekers are counted as the seeker index (Default for when there are no seekers)

Note! Attributes will be changed across games, so if you want to have the default values please backup the file before running the app!