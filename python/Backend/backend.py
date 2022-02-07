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


class Backend(Logger, SerialPort, Setup, Settings):

    onCreateLine = Signal(str,int)

    def __init__(self):
        Logger.__init__(self)
        SerialPort.__init__(self)
        Setup.__init__(self)
        Settings.__init__(self)
        self.cycleTimer = QTimer()
        self.cycleTimer.timeout.connect(self.loop_cbk)
        self.cycleTimer.start(1000)
        self.line: QtCharts.QLineSeries = []

        
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

    def loop_cbk(self):
        if self.setup_done_status:
            self.onCreateLine.emit("Testline", None)
            print("Line Created")
    
    @Slot(QObject)
    def add_line(self, line: QtCharts.QLineSeries):
        self.line.append(line)