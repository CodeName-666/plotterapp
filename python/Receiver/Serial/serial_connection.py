# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List
import serial
import serial.tools.list_ports
from Receiver.receiver import Receiver, ConnectionType
from Receiver.Serial.serial_config import SerialConfig
from PySide2.QtCore import QObject, Slot, Signal, QTimer


class SerialConnection(Receiver):
    def __init__(self, default_config: dict = None):
        Receiver.__init__(self, ConnectionType.SERIAL)
        self._serial = serial.Serial()
        self._config = None
        
        self.setup(default_config)
    
       
    def open_connection(self):
        if self._serial is not None:
            if not self._serial.isOpen():
                self._serial.open()

    def close_connection(self):
        if self._serial is not None:
            if self.is_connected():
                self._serial.close()

    def is_connected(self):
        return self._serial.isOpen()

    def setup(self, config: dict):
        self._config = SerialConfig(config)


