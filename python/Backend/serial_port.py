from distutils.log import Log
import typing
import serial
from serial.tools import list_ports
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtQml import QJSValue
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from Logger import logger

def get_serial_ports(): 
    ports = list_ports.comports()
    return [port.name for port in ports]


class SerialPort():
    
    comPortUpdate = Signal(dict)

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        self._com_updater_timer = QTimer()
        self.com_ports = []
        self._serial = serial.Serial()

        self.__init_update_timer()
    

    def __init_update_timer(self):
        self._com_updater_timer.timeout.connect(self.com_updater_cbk)
        self._com_updater_timer.start(1000)

    @property
    def com_ports(self):
        try:
            return self._com_list
        except:
            return None

    @com_ports.setter
    def com_ports(self, com_list):
        self._com_list = com_list

    def com_updater_cbk(self):
        new_com_list = get_serial_ports()
        if new_com_list != self.com_ports:
            logger.info("New Comports found {}".format(new_com_list))
            self.comPortUpdate.emit(new_com_list)
            self.com_ports = new_com_list
   
    # Obsolete Method
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




if __name__ == "__main__":
    
    @Slot(dict)
    def rxPortList(portList):
        print(portList)

    app = QApplication([]) # Start an application.
    window = QWidget() # Create a window.

    serial = SerialPort(None)
    serial.comPortUpdate.connect(rxPortList)
    window.show() # Show window
    app.exec_() # Execute the App
   