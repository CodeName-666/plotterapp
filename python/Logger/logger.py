import logging
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
import typing




class Logger(QObject):

    def __init__(self, parent: typing.Optional[QObject] = ..., config: dict = None) -> None:
        super().__init__(parent)
        if config:
            self.setup(config) 

    @property
    def enabled(self):
        try:
            return self._enabled
        except: 
            return False

    @enabled.setter
    def enabled(self, status):
        self._enabled = status   

    def setup(self, config: dict) -> None:
        self.enabled = config["enabled"]
        log_level = config["level"]
        name = config["name"]
        if self.enabled:
            logging.basicConfig(filename=name, encoding='utf-8',
                        format='%(asctime)s: %(levelname)s - %(message)s', level=log_level)

    
