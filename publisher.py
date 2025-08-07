import zmq

class ZMQPublisher:
    def __init__(self, port=5556):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")
        print(f"📡 ZMQ Publisher started at tcp://*:{port}")

    def publish(self, data):
        self.socket.send_json(data)
