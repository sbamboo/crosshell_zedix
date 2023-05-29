from ipc_json import JsonIPC

ipc = JsonIPC()
ipc.connect()

# Start the subscript process
ipc.start_subscript()

# Send some data to the subscript process
data = {"key": "value"}
ipc.send_json(data)

# Receive a response from the subscript process
response = ipc.recv_json()
print("Received response: ", response)

# Stop the subscript process once done using it
ipc.stop_subscript()