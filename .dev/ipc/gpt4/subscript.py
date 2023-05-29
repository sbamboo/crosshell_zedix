import json
import multiprocessing as mp

class Subscript:
    def __init__(self, send_queue, recv_queue):
        self.send_queue = send_queue
        self.recv_queue = recv_queue

    def run(self):
        while True:
            if not self.send_queue.empty():
                received_data = json.loads(self.send_queue.get())
                print("Subscript received data:", received_data)

                # Process the data, create a response
                response_data = {"response": "Processed"}

                # Send the response back to the caller
                self.recv_queue.put(json.dumps(response_data))