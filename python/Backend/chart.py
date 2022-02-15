
import typing
from PySide2.QtCore import QObject, Slot, Signal


class Chart():

    new_graph = Signal(str, int)

    def __init__(self, obj_name: str = "") -> None:
        obj_name = obj_name

    def setup(self, dict: typing.Dict):
        pass
