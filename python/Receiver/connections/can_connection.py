import can
from receiver_thread import ReceiverThread
from typing import Dict

class CanConnection(ReceiverThread):
    def __init__(self, channel, bustype):
        ReceiverThread.__init__(self)
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)


    def run(self):
        while not self.__stop:
            if not self._pause:
                message = self.bus.recv()
                self.new_data.emit(message)

    def send_response(self, response):
        self.bus.send(response)


    def connect(self):
        pass

    def disconnect(self):
        pass

    def connected(self):
        pass

    def config(self, config: Dict):
        pass