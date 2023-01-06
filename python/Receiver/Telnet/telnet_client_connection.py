# This Python file uses the following encoding: utf-8
from telnetlib import Telnet
from PySide6.QtCore import QObject, Slot, Signal,QThread
from .telnet_config import TelnetConfig


class TelnetClientConnection(QThread):
    def __init__(self, config: dict = None):
        QThread.__init__(self)
        self.telnet = Telnet()     
       #self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            data = self.telnet.read_all()
            self.parent.data.append(data)

    def send_response(self, response):
        self.telnet.write(response)
        

    def stop(self):
        self.stop_event.set()
        self.telnet.close()







    def open_connection(self):
        self.telnet.open(self.settings["host"], self.settings["port"])

    def close_connection(self):
        self.telnet.close()

    def is_connected(self):
        pass

    def setup(self, config: dict):
        self.__config = TelnetConfig(config)

