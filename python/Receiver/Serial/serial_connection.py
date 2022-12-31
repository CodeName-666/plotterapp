# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List
import serial
import serial.tools.list_ports
from Receiver.receiver import Receiver, ConnectionType
from Receiver.Serial.serial_config import SerialConfig
from PySide6.QtCore import QObject, Slot, Signal, QTimer


class SerialConnection(Receiver):
    def __init__(self, default_config: dict = None):
        Receiver.__init__(self, ConnectionType.SERIAL)
        self.__serial = serial.Serial()
        self.__config = None
        
        self.setup(default_config)
    
       
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


