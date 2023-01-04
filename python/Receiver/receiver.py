# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from enum import Enum


class ConnectionType(Enum):
    SERIAL = 1
    TELNET = 2
    NONE = 3


class Receiver:
    def __init__(self, receiver_thread):
        self.receiver_thread = receiver_thread
        self.data = []
        self.receiver_thread.parent = self
        self.receiver_thread.start()

    def get_data(self):
        return self.data

    def send_response(self, response):
        self.receiver_thread.send_response(response)

    def stop(self):
        self.receiver_thread.stop()

    def join(self):
        self.receiver_thread.join()

    def open_connection(self):
        pass

    def close_connection(self):
        pass

    def is_connected(self) -> bool:
        pass

    def settings_valid(self) -> bool:
        pass
