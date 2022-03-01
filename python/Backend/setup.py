
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property
import typing
from Logger import logger


class SetupSignals():
    setupUi = Signal(dict)


class Setup(SetupSignals):

    def __init__(self) -> None:
        self.__backend_setup_done = False
        self.__ui_setup_done = False
        self.__config = None

    @Property(bool)
    def backend_setup_done(self) -> bool:
        try: 
            return self.__backend_setup_done
        except:
            return False

    @backend_setup_done.setter
    def backend_setup_done(self, status: bool):
        self.__backend_setup_done = status
        logger.info("Backend Setup Status: {}".format(status))

    @Slot(bool)
    def ui_setup_done(self, status: bool):
        self.__ui_setup_done = status
        logger.info("Backend Setup Status: {}".format(status))

    def set_config(self, config: dict):
        self.__config = config
