import can
from receiver_thread import ReceiverThread


class CANReceiverThread(ReceiverThread):
    def __init__(self, channel, bustype):
        ReceiverThread.__init__(self)
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        #self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            message = self.bus.recv()
            self.parent.data.append(message)

    def send_response(self, response):
        self.bus.send(response)

    def stop(self):
        self.stop_event.set()

    def connect(self):
        pass

    def disconnect(self):
        pass

    def connected(self):
        pass