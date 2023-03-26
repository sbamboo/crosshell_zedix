import multiprocessing as mp

class Subscriber:
    def __init__(self, conn_in, conn_out):
        self.conn_in = conn_in
        self.conn_out = conn_out

    def run(self):
        while True:
            message = self.conn_in.recv()
            if message is None:
                break
            print(f"Received message: {message}")
            reply = f"Reply to {message}"
            self.conn_out.send(reply)
            print(f"Sent reply: {reply}")
        print("Subscriber done.")

if __name__ == "__main__":
    conn_in1, conn_out1 = mp.Pipe()
    conn_in2, conn_out2 = mp.Pipe()
    subscriber = Subscriber(conn_in2, conn_out1)
    subscriber_process = mp.Process(target=subscriber.run)
    subscriber_process.start()

    for i in range(5):
        message = f"Message {i}"
        conn_out2.send(message)
        print(f"Sent message: {message}")
        reply = conn_in1.recv()
        print(f"Received reply: {reply}")

    conn_out2.send(None)  # signal end of messages

    subscriber_process.join()
