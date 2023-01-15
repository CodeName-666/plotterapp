
# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject ,Slot, Signal, QTimer, Property,QJsonArray
from PySide6.QtQml import QJSValue
import typing
from Logger import logger
from Common.converter import Converter


class Setup():

    ui_setup = Signal('QVariant')
    ui_setup_done_changed = Signal(bool)
    backend_setup_done_changed = Signal(bool)

    def __init__(self) -> None:
        self.__config = None
        self.__ui_setup_done = False
        self.__backend_setup_done = False
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)

    @Property(bool)
    def backend_setup_done(self) -> bool:
        return self.__backend_setup_done 
        

    @backend_setup_done.setter
    def backend_setup_done(self, status: bool):
        if(self.__backend_setup_done != status):
            logger.log_info("Backend Setup Status: {}".format(status))
            self.__backend_setup_done = status
            self.backend_setup_done_changed.emit(status)

    @Property('bool')
    def ui_setup_done(self) -> bool:
        return self.__ui_setup_done

    @ui_setup_done.setter
    def ui_setup_done(self, status: bool):
        if(self.__ui_setup_done != status):
            logger.log_info("UI Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.ui_setup_done_changed.emit(status)

    def on_backend_setup_done(self, status: bool):
        if status:
            if not self.ui_setup_done:
                js_config = Converter.dict_to_jsvalue(self.ui_config)
                self.ui_setup.emit(self.ui_config)
            else:
                logger.log_info("UI already configured")
        else:
            logger.log_error("Cannot setup ui. Backend not configured")

    @property
    def ui_config(self) -> dict:
        return self.__config
            
    @ui_config.setter
    def ui_config(self, new_config: dict):
        self.__config = new_config
