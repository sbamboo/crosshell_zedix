import json
import multiprocessing as mp
from subscript import Subscript

class JsonIPC:
    def __init__(self):
        self.send_queue = None
        self.recv_queue = None
        self.subscript_process = None

    def connect(self):
        # Create communication queues
        self.send_queue = mp.Queue()
        self.recv_queue = mp.Queue()

    def send_json(self, data):
        # Send JSON data to subscript process
        if not self.subscript_process:
            raise RuntimeError("Subscript process not started")
        
        json_data = json.dumps(data)
                
        # Put in encode message and length 
        length=len(json_data)
        self.self.send_queue.put(json_data)

    def recv_json(self):
        # Receive JSON data from subscript process
        if not self.subscript_process:
            raise RuntimeError("Subscript process not started")
        
        while True:
            if not self.recv_queue.empty():
                json_data = self.recv_queue.get()
                return json.loads(json_data)

    def start_subscript(self):
        # Start the subscript process
        if not self.send_queue or not self.recv_queue:
            raise RuntimeError("Communication queues not initialized")

        subscript = Subscript(self.send_queue, self.recv_queue)
        self.subscript_process = mp.Process(target=subscript.run)
        self.subscript_process.start()

    def stop_subscript(self):
        # Stop the subscript process      
        if not self.subscript_process:
            raise RuntimeError('No SubScript Running')
        
        self.subsript_process.terminate()