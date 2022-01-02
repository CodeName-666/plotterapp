import typing
from plot import Plot
from PySide2.QtCore import QObject, Slot, Signal



class TimePlot(Plot):

    def __init__(self, parent: typing.Optional[QObject] = None) -> None:
        super().__init__(parent=parent)
