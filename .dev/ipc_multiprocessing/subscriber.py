import multiprocessing as mp

class Subscriber:
    def __init__(self, pipe):
        self.pipe = pipe

    def run(self):
        while True:
            message = self.pipe.recv()
            if message is None:
                break
            print(f"Received message: {message}")
        print("Subscriber done.")

if __name__ == "__main__":
    parent_conn, child_conn = mp.Pipe()
    subscriber = Subscriber(child_conn)
    subscriber_process = mp.Process(target=subscriber.run)
    subscriber_process.start()

    for i in range(5):
        message = f"Message {i}"
        parent_conn.send(message)
        print(f"Sent message: {message}")

    parent_conn.send(None)  # signal end of messages

    subscriber_process.join()
