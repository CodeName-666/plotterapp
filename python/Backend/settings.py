# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
import typing


class Settings(QObject):

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        super().__init__(parent)