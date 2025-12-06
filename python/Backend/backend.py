# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QJsonValue
from PySide6.QtQml import QJSValue
from PySide6 import QtCharts
from typing import Dict

from Receiver.receiver import Receiver
from Receiver.registry import ReceiverRegistry, parse_interface_definitions

# Backend interfaces
from .settings import Settings
from .serial_port import SerialPort
from .setup import Setup
from Logger import logger
from Logger.logger import Logger
from .chart import Chart


class Backend(Settings, Logger, SerialPort, Setup, Chart):

    __backend_instance = None

    def __init__(self):
        if Backend.__backend_instance != None:
            pass
        else:
            Settings.__init__(self)
            Logger.__init__(self)
            SerialPort.__init__(self)
            Setup.__init__(self)
            Chart.__init__(self)
            self.receiver_list: Dict[str, Receiver] = {}
            self.__receiver_registry = ReceiverRegistry()
            self.__interfaces_config = {}
            Backend.__backend_instance = self
            # self.connect_signals()

    @staticmethod
    def get_instance():
        if Backend.__backend_instance == None:
            Backend()
        return Backend.__backend_instance

    def connect_signals(self):
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)

    @Slot('str', result='bool')
    def connectTo(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            if self.receiver_list[connection_type].settings_valid():
                if not self.receiver_list[connection_type].is_connected():
                    if self.receiver_list[connection_type].open_connection():
                        return True
                    else:
                        logger.log_error("Cannot open connection, undef error")
                        return False
                else:
                    logger.log_info("Allready Connected")
                    return False
            else:
                logger.log_warning("Invalid settings")
                return False
        else:
            logger.log_error("Invalid Connection type")
            return False

    def config(self, config: dict):
        if not config:
            logger.log_error("Backend configuration missing")
            return

        Setup.ui_config = config.get("qml", {})
        self.__interfaces_config = parse_interface_definitions(
            config.get("interfaces", [])
        )
        self.receiver_list = self.__receiver_registry.create_receivers(
            self.__interfaces_config.values()
        )

        logger.log_info(
            "Backend registered %s receiver(s)",
            len(self.receiver_list.keys()),
        )
