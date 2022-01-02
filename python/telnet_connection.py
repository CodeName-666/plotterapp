# This Python file uses the following encoding: utf-8
from telnetlib import Telnet
from receiver import Receiver, ConnectionType
from PySide2.QtCore import QObject, Slot, Signal


class TelnetConfig(QObject):

    def __init__(self, default_config: dict = None):
        super(TelnetConfig, self).__init__()
        self.port = 0
        self.url = ""


    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: dict):
        self._config = config

    def config(self, url: str, port: int):
        self._config["url"] = url
        self._config["port"] = port


class TelnetConnection(Receiver):
    def __init__(self, config: dict = None):
        Receiver.__init__(self, ConnectionType.TELNET)
        self.telnet = Telnet()
        # Set TelnetSettings directly an not through constructor with default config, if
        # telnet_settings == None
        self.config = TelnetConfig()
       

    def open_connection(self):
        self.telnet.open(self.settings["host"], self.settings["port"])

    def close_connection(self):
        self.telnet.close()

    def is_connected(self):
        pass
