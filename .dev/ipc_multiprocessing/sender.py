import multiprocessing as mp

class Sender:
    def __init__(self, pipe):
        self.pipe = pipe

    def run(self):
        for i in range(5):
            message = f"Message {i}"
            self.pipe.send(message)
            print(f"Sent message: {message}")
        self.pipe.send(None)  # signal end of messages
        print("Sender done.")

if __name__ == "__main__":
    parent_conn, child_conn = mp.Pipe()
    sender = Sender(child_conn)
    sender_process = mp.Process(target=sender.run)
    sender_process.start()

    while True:
        message = parent_conn.recv()
        if message is None:
            break
        print(f"Received message: {message}")

    sender_process.join()
