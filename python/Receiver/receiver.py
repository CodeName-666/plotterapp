# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot
from enum import Enum
from typing import Dict
from receiver_thread import ReceiverThread


class Receiver:
    def __init__(self, receiver_thread: ReceiverThread = None) -> None:
        self.receiver_thread: ReceiverThread = receiver_thread
        self.data = []
  
    @Slot(bytes)
    def new_data(self, data: bytes):
        self.data.append(data)

    def get_data(self):
        return self.data

    def send_response(self, response):
        if self.receiver_thread:
            self.receiver_thread.send_response(response)
        else: 
            pass

    def stop(self):
        if self.receiver_thread:
            self.receiver_thread._stop()
        else: 
            pass

    def start(self): 
        if self.receiver_thread:
            self.receiver_thread.start()

    def join(self):
        if self.receiver_thread:
            self.receiver_thread.join()
        else:
            pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def connected(self) -> bool:
        pass

    def config(self, config: Dict): 
        pass

    def settings_valid(self) -> bool:
        pass
