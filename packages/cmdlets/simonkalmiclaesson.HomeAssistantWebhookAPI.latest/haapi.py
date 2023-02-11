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
    "balkongen.socket1": "switch.balkongen_socket_1",
    "sovrum.fonsterlampa": "switch.fonster_lampan",
    "vardagsrum.fonsterlampa": "switch.fonsterlampa_vardagsrum_socket_1",
    "kok.fonsterlampa": "switch.koket",
    "sovrum.skrivaren": "switch.skrivaren",
    "sovrum2.sangbord": "switch.sovrum2_fonster",
    "sovrum.sanglampa": "switch.sangbord",
    "sovrum.tvsystem": "switch.tv_system",

    "sovrum.lampa2": "light.lampa_2",
    "sovrum.lampa4": "light.lampa_4",
    "hallen.lampac": "light.lampa_c",
    "sovrum.lampaS": "light.lampa_s",
    "sovrum.ledlist": "light.led_list_sovrum",
    "sovrum2.fonsterlampa": "light.sovrum2",
    "sovrum2.byralampa": "light.sovrum_2b",
    "sovrum2.taklampa": "light.sovrum2d",

    "sovrum": "light.lampor_i_sovrum",
    "sovrum2": "light.lampor_i_sovrum2",
    "sovrum.taklampa": "light.taklampa",
    "vardagsrum": "light.vardagsrum",
    "vardagsrum.taklampa": "light.taklampa_vardagsrum"
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