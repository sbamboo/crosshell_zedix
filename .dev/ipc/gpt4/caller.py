import json
import multiprocessing as mp
from subscript import Subscript

def main():
    # Create communication queues
    send_queue = mp.Queue()
    recv_queue = mp.Queue()

    # Start the subscript process
    subscript = Subscript(send_queue, recv_queue)
    subscript_process = mp.Process(target=subscript.run)
    subscript_process.start()

    # Send and receive JSON data
    data_to_send = {"key": "value"}
    send_queue.put(json.dumps(data_to_send))

    while True:
        if not recv_queue.empty():
            received_data = json.loads(recv_queue.get())
            print("Received data:", received_data)
            break

    subscript_process.terminate()

if __name__ == "__main__":
    main()