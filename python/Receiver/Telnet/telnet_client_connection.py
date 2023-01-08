# This Python file uses the following encoding: utf-8
from telnetlib import Telnet
from typing import Dict
from .telnet_config import TelnetConfig
from receiver_thread import ReceiverThread



class TelnetClientConnection(ReceiverThread):
    def __init__(self, config: dict = None):
        ReceiverThread.__init__(self)
        self.telnet = Telnet()     
       #self.stop_event = threading.Event()

    def init(self, config: Dict):
        pass

    def run(self):
        while not self.stop_event.is_set():
            data = self.telnet.read_all()
            self.parent.data.append(data)

    def send_response(self, response):
        self.telnet.write(response)
        

    def stop(self):
        self.stop_event.set()
        self.telnet.close()

    def conect(self):
        self.telnet.open(self.settings["host"], self.settings["port"])

    def disconnect(self):
        self.telnet.close()

    def connected(self):
        pass

    def setup(self, config: dict):
        self.__config = TelnetConfig(config)

