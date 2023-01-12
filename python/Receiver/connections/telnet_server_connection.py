

from typing import Dict
from receiver_thread import ReceiverThread
from telnetlib import Telnet
from .config.telnet_config import TelnetConfig



class TelnetServerThread(ReceiverThread):

    def __init__(self) -> None:
        ReceiverThread.__init__(self)
        self.telnet = Telnet()

    def run(self):
        pass

    def send_response(self, response):
        pass

    def stop(self):
        pass

    def connect(self):
        pass
    
    def disconnect(self):
        pass
    
    def connected(self):
        pass

    def config(self, config: Dict):
        pass

    
server = telnetlib.Telnet()
server.bind((HOST, PORT))
server.listen(1)
