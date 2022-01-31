
import typing
from PySide2.QtCore import QObject, Slot, Signal


class Plot(QObject):

    def __init__(self, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent=parent)
        self.name = ""

    @property    
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
