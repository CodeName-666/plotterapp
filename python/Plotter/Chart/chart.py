
import typing
from unittest import expectedFailure
from PySide2.QtCore import QObject, Slot, Signal


class Chart():

    def __init__(self, obj_name: str = "") -> None:
        obj_name = obj_name

    @property
    def object_name(self) -> str:
        try:
            return self._object_name
        except:
            return ""
    
    @object_name.setter
    def object_name(sefl, obj_name: str):
        self._object_name = obj_name

    @property
    def root_context(self):
        try:
            return self._root_context
        except:
            return None

    @root_context.setter
    def root_context(self, root):
        self._root_context = root

    def setup(self, dict: typing.Dict):
        pass
