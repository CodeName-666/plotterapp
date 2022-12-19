# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from enum import Enum


class ConnectionType(Enum):
    SERIAL = 1
    TELNET = 2
    NONE = 3


class Receiver(QtCore.QThread):
    def __init__(self, receiver_type: ConnectionType, receiver_settings=None):
        self.config = receiver_settings
        self.type = receiver_type

    @property
    def type(self) -> ConnectionType:
        return self.__type

    @type.setter
    def type(self, type: ConnectionType):
        self.__type = type

    def open_connection(self):
        pass

    def close_connection(self):
        pass

    def is_connected(self) -> bool:
        pass

    def settings_valid(self) -> bool:
        pass
