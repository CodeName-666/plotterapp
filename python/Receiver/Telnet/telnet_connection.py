# This Python file uses the following encoding: utf-8
from telnetlib import Telnet
from Receiver.receiver import Receiver, ConnectionType
from PySide6.QtCore import QObject, Slot, Signal
from .telnet_config import TelnetConfig


class TelnetConnection(Receiver):
    def __init__(self, config: dict = None):
        Receiver.__init__(self, ConnectionType.TELNET)
        self.telnet = Telnet()
        self.__config = None
        self.setup(config)

    def open_connection(self):
        self.telnet.open(self.settings["host"], self.settings["port"])

    def close_connection(self):
        self.telnet.close()

    def is_connected(self):
        pass

    def setup(self, config: dict):
        self.__config = TelnetConfig(config)

