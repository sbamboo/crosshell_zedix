import json

class Subscript:
    def __init__(self, send_queue, recv_queue):
        self.send_queue = send_queue
        self.recv_queue = recv_queue

    def run(self):
        while True:
            if not self.send_queue.empty():
                # Receive JSON data from caller process
                json_data = self.send_queue.get()

                # Do something with incoming JSON data...
                data = json.loads(json_data)
                print("Received: ", data)

                # Send a response back to the caller process
                response_data = {"response": "acknowledged"}
                response_json_data = json.dumps(response_data)
                
                # Encode message and length before sending it through the queue.
                length=len(response_json_data)
                self.recv_queue.put(f"{length}:{response_json_data}")