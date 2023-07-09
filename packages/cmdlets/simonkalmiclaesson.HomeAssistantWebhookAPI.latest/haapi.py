# [Imports]
import uuid
import requests
import argparse
from assets.lib.filesys import filesys as fs

# [Arguments]
cparser = argparse.ArgumentParser(prog="HomeAssistant-Webhook",exit_on_error=False,add_help=False)
cparser.add_argument('--exhelp', action='store_true', default=False, help='Shows help then exits.')
cparser.add_argument('-h', '--help', action='store_true', default=False, help='Shows help menu.')
cparser.add_argument('-s','-shortsyntax', dest="shortsyntax", help="Supply a short syntax (<group>.<name>:<action>)")
cparser.add_argument('-device', dest="device", help="Device to use (<group>.<name>)")
cparser.add_argument('-action', dest="action", help="Action to do to device ('turn_on' or 'turn_off', 'brightness:<precentage>', 'kelvin:<temprature.kelvin>')")
cparser.add_argument('--list', dest="list", action="store_true", help="Lists out devices.")
cparser.add_argument('--genid', dest="genid", action="store_true", help="Generate a id number to be used with webhooks")
# Create main arguments object
try: argus = cparser.parse_args(argv)
except: argus = cparser.parse_args()
if argus.help: cparser.print_help()
if argus.exhelp: cparser.print_help(); exit()

# [Setup]
haapi_version = "1.0"

# [Setup WebHook-API]
webhook_url_file = f"{CSScriptRoot}{os.sep}url.localcfg"
if os.path.exists(webhook_url_file):
    api_access_url = open(webhook_url_file).read()
else:
    api_access_url = input("No url config file found please write webhook url to save: ")
    fs.writeToFile(api_access_url,webhook_url_file,autocreate=True)
localcopy_devices = {
    "balkong.utag": "switch.balkongutag_socker_1",
    #"sovrum.fonsterlampa": "switch.fonster_lampan",
    "vardagsrum.fonster": "switch.fonsterlampa_vardagsrum_socket_1",
    "kok.utag": "switch.kok_utag",
    #"sovrum.skrivaren": "switch.skrivaren",
    #"sovrum.tvsystem": "switch.tv_system",

    #"sovrum.sangbord": "light.sv2_sangbord",
    "sovrum.takH": "light.sv1_takhoger",
    "sovrum.takM": "light.sv1_takmitt",
    "sovrum.takV": "light.sv1_takvanster",
    #"sovrum.lampaS": "light.lampa_s",
    #"sovrum.ledlist": "light.led_list_sovrum",
    "sovrum2.byra": "light.sv2_byra",
    "sovrum2.tak": "light.sv2_tak",
    "sovrum2.fonster": "light.sv2_fonster",
    "sovrum2.sangbord": "light.sv2_sangbord",
    "hall.tak": "light.hall_tak",
    "vardagsrum.bord": "light.va_bordslampa",
    "vardagsrum.horn": "light.va_hornlampa",
    "vardagsrum.soff": "light.va_sofflampa",
    "vardagsrum.tak": "light.va_taklampa",
    "vardagsrum.tak1": "light.va_tak1",
    "vardagsrum.tak2": "light.va_tak2",
    "vardagsrum.tak3": "light.va_tak3",
    "vardagsrum.tak4": "light.va_tak4",
    "vardagsrum.tak5": "light.va_tak5"
}

# [List devices]
if argus.list:
    print(f"  Local copy of devices for version {haapi_version}")
    print( "-----------------------------------------")
    for key in localcopy_devices: print(key)

# [GenId]
elif argus.genid: print(((str(uuid.uuid4()) + str(uuid.uuid4())).replace("-","")).strip())

# [Send request]
else:
    if argus.shortsyntax:
        req = (':'.join(argus.shortsyntax.split(':')[1:])).strip(":")
        if "bright:" in req: req = req.replace("bright:","brightness:")
        if "tempk:" in req: req = req.replace("tempk:","kelvin:")
        payload = f"ClientApiVersion={haapi_version},Device={argus.shortsyntax.split(':')[0]},Requests={req}"
    else:
        payload = f"ClientApiVersion={haapi_version},Device={argus.device},Requests={argus.action}"
    print(payload)
    requests = requests.post(api_access_url, data=payload)