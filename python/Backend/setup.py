
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property, QJsonValue
from PySide2.QtQml import QJSValue
import typing
from Logger import logger
from Common.converter import Converter


class Setup(Converter):

    ui_setup = Signal(QJSValue)
    ui_setup_done_changed = Signal(bool)
    backend_setup_done_changed = Signal(bool)

    def __init__(self) -> None:
        Converter.__init__(self)
        self.ui_config = None
        self.backend_setup_done = False
        self.ui_setup_done = False
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)

    @Property(bool)
    def backend_setup_done(self) -> bool:
        try:
            return self.__backend_setup_done
        except:
            return False

    @backend_setup_done.setter
    def backend_setup_done(self, status: bool):
        if(self.backend_setup_done != status):
            logger.info("Backend Setup Status: {}".format(status))
            self.__backend_setup_done = status
            self.backend_setup_done_changed.emit(status)

    @Property(bool)
    def ui_setup_done(self) -> bool:
        try:
            return self.__ui_setup_done
        except:
            return False

    @ui_setup_done.setter
    def ui_setup_done(self, status: bool):
        if(self.ui_setup_done != status):
            logger.info("UI Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.ui_setup_done_changed.emit(status)

    def on_backend_setup_done(self, status: bool):
        if status:
            if not self.ui_setup_done:
                js_config = self.dict_to_jsvalue(self.ui_config)
                self.ui_setup.emit(js_config)
            else:
                logger.info("UI already configured")
        else:
            logger.error("Cannot setup ui. Backend not configured")

    @property
    def ui_config(self) -> dict:
        try:
            return self.__config
        except:
            return None

    @ui_config.setter
    def ui_config(self, new_config: dict):
        self.__config = new_config
