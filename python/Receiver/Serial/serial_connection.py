# This Python file uses the following encoding: utf-8
import sys
import glob
import logging

from typing import List
import serial
import serial.tools.list_ports
from receiver import Receiver, ConnectionType
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

def DictValue2Key(dictionary: dict, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.name for port in ports]



class SerialConfig(QObject):
    _com_updater_signal = Signal()

    def __init__(self, default_config: dict):
        super(SerialConfig, self).__init__()

        self._port = ""
        self._baud = 0
        self._size = 0
        self._parity = 0
        self._stopbits = 0

        self._com_available_list = []
        self._com_updater_timer = QTimer()
        self.__init_update_timer()

        self.com_list = []
        self.config = default_config

    def __init_update_timer(self):
        self._com_updater_timer.timeout.connect(self.com_updater_cbk)
        self._com_updater_timer.start(1000)

    def load(self):
        self._com_list = self.create_com_list()

    @property
    def com_list(self):
        return self._com_list

    @com_list.setter
    def com_list(self, com_list):
        self._com_list = com_list

    def com_updater_cbk(self):
        print("CaLLBack Call")
        new_com_list = get_serial_ports()
        if new_com_list != self._com_available_list:
            print("Emit signal")
            self._com_list = get_serial_ports()
            self._com_updater_signal.emit()
            self._com_available_list = new_com_list

    #def create_com_list():
    #    com_port_list = []
    #    available_com_ports = SerialConfig.serial_ports()
    #    for k in available_com_ports:
    #        print("New Port {}".format(k))
#
    #    for i in range(1, 10):
    #        port = 'COM{}'.format(i)
    #        if port in available_com_ports:
    #            port = port + ': [x]'
#
    #        com_port_list.append(port)
    #    return com_port_list

    @property
    def config(self) -> dict:
        config = {
            "port"     : self._port,
            "baud"     : self._baud,
            "size"     : DictValue2Key(SerialSize,self._size),
            "parity"   : DictValue2Key(SerialParity, self._parity),
            "stop_bits": DictValue2Key(SerialStopBits, self._stopbits)
        }
        return config

    @config.setter
    def config(self, config: dict):
        self._port = config["port"]
        self._baud = config["baud"]
        self._size = SerialSize[config["size"]]
        self._parity = SerialParity[config["parity"]]
        self._stopbits = SerialStopBits[config["stop_bits"]]
        
   


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
