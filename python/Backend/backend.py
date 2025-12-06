# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QJsonValue
from PySide6.QtQml import QJSValue
from PySide6 import QtCharts
from typing import Dict

from Receiver.receiver import Receiver
from Receiver.registry import ReceiverRegistry, parse_interface_definitions
from Common.converter import Converter

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
        receiver = self.receiver_list.get(connection_type)
        if receiver is None:
            logger.log_error("Invalid Connection type: %s", connection_type)
            return False

        try:
            receiver.start()
        except ValueError as exc:
            logger.log_warning("Receiver settings invalid: %s", exc)
            return False
        except ConnectionError as exc:
            logger.log_error("Unable to open receiver connection: %s", exc)
            return False

        logger.log_info("Receiver %s started", connection_type)
        return True

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

    @Slot('QString', 'QJSValue', result='bool')
    def set_settings(self, interface: str, settings: QJSValue) -> bool:
        Settings.set_settings(self, interface, settings)
        receiver = self.receiver_list.get(interface)
        if receiver is None:
            logger.log_warning("set_settings: Unknown interface %s", interface)
            return False

        py_settings = Converter.jsvalue_to_dict(settings)
        if not isinstance(py_settings, dict):
            logger.log_warning("set_settings: Cannot convert settings for %s", interface)
            return False

        receiver.config(py_settings)
        logger.log_info("Updated settings for %s", interface)
        return True
