# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
from Receiver.receiver import Receiver
from PySide2.QtCharts import QtCharts


# Backend interfaces
from .settings import Settings
from .serial_port import SerialPort
from .setup import Setup
from Logger import logger
from Logger.logger import Logger
from .chart import Chart

class Backend(Logger, SerialPort, Setup, Chart, Settings):

    __backend_instance = None

    def __init__(self):
        if Backend.__backend_instance != None:
            pass
        else:
            Logger.__init__(self)
            SerialPort.__init__(self)
            Setup.__init__(self)
            Chart.__init__(self)
            Settings.__init__(self)
            Backend.__backend_instance = self

    
    @staticmethod
    def get_instance():
        if Backend.__backend_instance == None:
            Backend()
        return Backend.__backend_instance

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

    def config(self, config: dict):
        Setup.config(config["qml"])