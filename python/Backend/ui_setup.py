
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
import typing
from Logger import logger


class UiSetup(QObject):

    def __init__(self, parent: typing.Optional[QObject] = None) -> None:
        super(UiSetup, self).__init__()
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

    @Slot(bool)
    def setup_done(self, status: bool):
        self.setup_done_status = status
        logger.info("Backend setup done")

