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

    
class SerialConfig(QObject):

    def __init__(self, default_config: dict):
        super(SerialConfig, self).__init__()

        self._port: str = ""
        self._baud: int = 0
        self._size: int = 0
        self._parity: float = 0
        self._stopbits: str = 0

        self._com_available_list = []
        self._com_updater_timer = QTimer()
        self.__init_update_timer()

        self.com_list = []
        self.setup = default_config

    def load(self):
        self._com_list = self.create_com_list()

 
    @property
    def setup(self) -> dict:
        return {
            "port"     : self._port,
            "baud"     : self._baud,
            "size"     : DictValue2Key(SerialSize,self._size),
            "parity"   : DictValue2Key(SerialParity, self._parity),
            "stop_bits": DictValue2Key(SerialStopBits, self._stopbits)
        }
        

    @setup.setter
    def setup(self, config: dict):
        self._port = config["port"]
        self._baud = config["baud"]
        self._size = SerialSize[config["size"]]
        self._parity = SerialParity[config["parity"]]
        self._stopbits = SerialStopBits[config["stop_bits"]]
        
   
