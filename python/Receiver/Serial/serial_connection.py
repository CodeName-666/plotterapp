# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List
import serial
import serial.tools.list_ports
from receiver import Receiver, ConnectionType
from serial_config import SerialConfig
from PySide2.QtCore import QObject, Slot, Signal, QTimer


SerialSize = {
    '5Bit': serial.FIVEBITS, 
    '6Bit': serial.SIXBITS, 
    '7Bit': serial.SEVENBITS, 
    '8Bit': serial.EIGHTBITS
}

SerialStopBits = {
    '1Bit'  : serial.STOPBITS_ONE, 
    '1.5Bit': serial.STOPBITS_ONE_POINT_FIVE, 
    '2Bit'  : serial.STOPBITS_TWO
}

SerialParity = {
    'None' : serial.PARITY_NONE, 
    'Even' : serial.PARITY_EVEN, 
    'Odd'  : serial.PARITY_ODD, 
    'Mark' : serial.PARITY_MARK, 
    'Space': serial.PARITY_SPACE
}




class SerialConnection(Receiver):
    def __init__(self, default_config: dict = None):
        Receiver.__init__(self, ConnectionType.SERIAL)
        self._serial = serial.Serial()
        self.config = SerialConfig(default_config)
       
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
