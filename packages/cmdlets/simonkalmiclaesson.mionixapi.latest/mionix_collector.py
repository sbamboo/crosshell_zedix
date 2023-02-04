import os
try:
    import websocket
except:
    os.system("python3 -m pip install websocket-client")
    import websocket

import json

ws = websocket.create_connection("ws://localhost:7681", subprotocols=["mionix-beta"])
ws.settimeout(5) # set timeout to 5 seconds


# Send a message over the WebSocket connection
ws.send("crosshell.mionixAPI.connection_send")

# Continuously receive and print messages from the server
completeResponse = []
print("Start the collection then plug in and out the mouse, waiting around a second inbetween, for slower systems wait a bit longer.")
_ = input("Press enter to start...")
print("Collection started...")
loops = 100
while loops > 0:
    response = json.loads(ws.recv())
    if response["type"] == "devices":
        if len(response) <= 1:
            if (response["type"] + "'}]") not in str(completeResponse):
                completeResponse.append( response )
        else:
            if (response["type"] + "': ") not in str(completeResponse):
                completeResponse.append( response )
    if response["type"] not in str(completeResponse):
        completeResponse.append( response )
    loops = loops - 1

# Close the WebSocket connection
ws.close()

# Set the basedata
print("Done!")
basedata = completeResponse


# Print basedata
print(basedata)