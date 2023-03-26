import multiprocessing as mp

class Sender:
    def __init__(self, conn_in, conn_out):
        self.conn_in = conn_in
        self.conn_out = conn_out

    def run(self):
        for i in range(5):
            message = f"Message {i}"
            self.conn_out.send(message)
            print(f"Sent message: {message}")
            reply = self.conn_in.recv()
            print(f"Received reply: {reply}")
        self.conn_out.send(None)  # signal end of messages
        print("Sender done.")

if __name__ == "__main__":
    conn_in1, conn_out1 = mp.Pipe()
    conn_in2, conn_out2 = mp.Pipe()
    sender = Sender(conn_in1, conn_out2)
    sender_process = mp.Process(target=sender.run)
    sender_process.start()

    while True:
        message = conn_in2.recv()
        if message is None:
            break
        print(f"Received message: {message}")
        reply = f"Reply to {message}"
        conn_out1.send(reply)
        print(f"Sent reply: {reply}")

    sender_process.join()
