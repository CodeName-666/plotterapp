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

    com_port_update = Signal('QVariant')

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        self.__com_updater_timer = QTimer()
        self.com_ports = []
        self.__serial = serial.Serial()

        self.__init_update_timer()

    def __init_update_timer(self):
        self.__com_updater_timer.timeout.connect(self.com_updater_cbk)
        self.__com_updater_timer.start(1000)

    @property
    def com_ports(self):
        try:
            return self.__com_list
        except:
            return None

    @com_ports.setter
    def com_ports(self, com_list):
        self.__com_list = com_list

    def com_updater_cbk(self):
        new_com_list = get_serial_ports()
        if new_com_list != self.com_ports:
            logger.info("New Comports found {}".format(new_com_list))
            self.com_port_update.emit(new_com_list)
            self.com_ports = new_com_list


if __name__ == "__main__":

    @Slot(dict)
    def rxPortList(portList):
        print(portList)

    app = QApplication([])  # Start an application.
    window = QWidget()  # Create a window.

    serial = SerialPort(None)
    serial.com_port_update.connect(rxPortList)
    window.show()  # Show window
    app.exec_()  # Execute the App
