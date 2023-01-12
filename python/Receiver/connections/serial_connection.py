# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List, Dict
import serial
import serial.tools.list_ports
from Receiver.Serial.serial_config import SerialConfig
from receiver_thread import ReceiverThread


class SerialReceiverThread(ReceiverThread):
    def __init__(self, port, baudrate):
        ReceiverThread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port, self.baudrate)
        #self.stop_event = threading.Event()

    def run(self):
        while not self._stop:
            if not self._pause:
                data = self.serial.readline()
                self.parent.data.append(data)
            else:
                pass

    def send_response(self, response):
        self.serial.write(response)

    def stop(self):
        self.stop_event.set()
        self.serial.close() 
       
    def connect(self):
        if self.__serial is not None:
            if not self.__serial.isOpen():
                self.__serial.open()

    def disconnect(self):
        if self.__serial is not None:
            if self.connected():
                self.__serial.close()

    def connected(self):
        return self.__serial.isOpen()

    def config(self, config: Dict):
        self.__config = SerialConfig(config)


