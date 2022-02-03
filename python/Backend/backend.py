# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
from python.Receiver.receiver import Receiver


# Backend interfaces
from .settings import Settings
from .serial_port import SerialPort
from .ui_setup import UiSetup
from python.Logger import logger
from python.Logger.logger import Logger



class Backend(Settings, SerialPort, UiSetup, Logger):

    def __init__(self):
        super(Settings, self).__init__()
        super(SerialPort, self).__init__()
        super(UiSetup, self).__init__()
        super(Logger, self).__init__()

    @property
    def receiver(self):
        try:
            return self._receiver
        except:
            return None

    @receiver.setter
    def receiver(self, receiver: Receiver) -> int:
        self._receiver = receiver

    @Slot('str', result='bool')
    def connect(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            if self.receiver_list[connection_type].settings_valid():
                if not self.receiver_list[connection_type].is_connected():
                    if self.receiver_list[connection_type].open_connection():
                        return True
                    else:
                        logger.error("Cannot open connection, undef error")
                        return False
                else:
                    logger.info("Allready Connected")
                    return False
            else:
                logger.warning("Invalid settings")
                return False
        else:
            logger.error("Invalid Connection type")
            return False

    @Slot('str', result='bool')
    def settings_valid(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            return self.receiver_list[connection_type].settings_valid()
        else:
            return False
