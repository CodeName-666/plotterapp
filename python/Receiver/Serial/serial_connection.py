# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List
import serial
import serial.tools.list_ports
from Receiver.receiver import Receiver, ConnectionType
from Receiver.Serial.serial_config import SerialConfig
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QThread


class SerialReceiverThread(QThread):
    def __init__(self, port, baudrate):
        QThread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port, self.baudrate)
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            data = self.serial.readline()
            self.parent.data.append(data)

    def send_response(self, response):
        self.serial.write(response)

    def stop(self):
        self.stop_event.set()
        self.serial.close()

    
       
    def open_connection(self):
        if self.__serial is not None:
            if not self.__serial.isOpen():
                self.__serial.open()

    def close_connection(self):
        if self.__serial is not None:
            if self.is_connected():
                self.__serial.close()

    def is_connected(self):
        return self.__serial.isOpen()

    def setup(self, config: dict):
        self.__config = SerialConfig(config)


