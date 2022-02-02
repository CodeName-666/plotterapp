
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
import typing


class UiSetup(QObject):

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        super().__init__(parent)
        self.setup_done_status = False

    @property
    def setup_done_status(self): 
        try:
            return self._setup_done_status
        except:
            return False 

    @setup_done_status.setter
    def setup_done_status(self, status): 
        self._setup_done_status = status

    def setup_done(self):
        self.setup_done_status = True
