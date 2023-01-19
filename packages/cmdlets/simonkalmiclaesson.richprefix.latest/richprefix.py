# [Imports]
from assets.lib.simpleDownload import *
import argparse

# [Arguments]
cparser = argparse.ArgumentParser(prog="richprefix",exit_on_error=False,add_help=False)
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
# Arguments
cparser.add_argument('-l','-load', dest="load", help="Preset to load")
cparser.add_argument('--debug', dest="debug", action='store_true', help="Debug")
# Options (Comsume al remaining arguments)
cparser.add_argument('options', nargs='*')
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()

# get presets
if os.path.exists(f"{CSScriptRoot}\presets.list") == True:
    presents_content_local = getContent(f"{CSScriptRoot}\presets.list")
presets_content_online = simpleDownload("https://raw.githubusercontent.com/simonkalmiclaesson/packagehand_repository/main/repository/cmdlet/_private/private_richprefix/presets.list","")
if "# format" in (presets_content_online.decode()).split("\n")[0]:
    presets_content = (presets_content_online.decode()).split("\n")
else:
    presets_content = (presets_content_online.decode()).split("\n")

richprefix = cs_persistance("get","cs_prefix",cs_persistanceFile)

load = int(argus.load)

if load != "" and load != None and load != int():
    if load != "0":
        if load > (len(presets_content)-1):
            print(pt_format(cs_palette,f"\033[31mNo preset with index '{load}'\033[0m"))
        else:
            richprefix = presets_content[load]

    if argus.debug == True: print(pt_format(cs_palette,f"\033[32m{richprefix}\033[0m"))
    if load <= (len(presets_content)-1):

        #Apply prefix
        csshell_prefix = richprefix.strip("'")
        cs_persistance("set","cs_prefix",cs_persistanceFile,csshell_prefix)
    


    