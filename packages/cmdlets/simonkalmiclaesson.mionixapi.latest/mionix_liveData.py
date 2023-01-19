try:
    import websocket
except:
    os.system("python3 -m pip install websocket-client")
    import websocket

import json
from assets.lib.drawlib.base import fill_terminal

ws = websocket.create_connection("ws://localhost:7681", subprotocols=["mionix-beta"])


# Send a message over the WebSocket connection
ws.send("crosshell.mionixAPI.connection_send")

# Continuously receive and print messages from the server
fill_terminal(" ")
deviceState = None
last_bioMetrics = None
last_bioRaw = None
last_mouseMetrics = None
print(pt_format(cs_palette,"\033[1;1H\033[34mMouse Data: (Press Ctrl+C to exit)\033[0m"))
print(pt_format(cs_palette,"\033[2;1H\033[34m--------------------------------------"))
print(pt_format(cs_palette,f"\033[3;1H\033[33mLastDeviceState: {str(deviceState)}\033[0m                                                       "))
while True:
    response = json.loads(ws.recv())
    if response == None or response == {}:
        response["type"] = None
    if response["type"] == "bioMetrics":
        print(pt_format(cs_palette,f"\033[5;1H\033[32mBioMetrics: {response}\033[0m                                                       "))
        last_bioMetrics = response
    elif response["type"] == "bioRaw":
        print(pt_format(cs_palette,f"\033[8;1H\033[32mBioRaw: {response}\033[0m                                                       "))
        last_bioRaw = response
    elif response["type"] == "mouseMetrics":
        print(pt_format(cs_palette,f"\033[10;1H\033[32mMouseMetrics: {response}\033[0m                                                       "))
        last_mouseMetrics = response
    elif response["type"] == "devices":
        if len(response) > 1:
            deviceState = "Connected"
        else:
            deviceState = "Disconnected"
            print(pt_format(cs_palette,f"\033[5;1H\033[31mBioMetrics: {str(last_bioMetrics)}\033[0m                                                       "))
            print(pt_format(cs_palette,f"\033[8;1H\033[31mBioRaw: {str(last_bioRaw)}\033[0m                                                       "))
            print(pt_format(cs_palette,f"\033[10;1H\033[31mMouseMetrics: {str(last_mouseMetrics)}\033[0m                                                                                                                                                                                                                                                                                                                                          "))
        print(pt_format(cs_palette,f"\033[3;1H\033[33mLastDeviceState: {str(deviceState)}\033[0m                                                       "))
# Close the WebSocket connection
ws.close()