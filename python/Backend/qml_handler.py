from ast import expr_context
from logging import root
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal
import typing




class QML_Handler:

    def __init__(self, qml_app_engine: QQmlApplicationEngine = None ) -> None:
        pass

    @property
    def qml_application_engine(self) -> QQmlApplicationEngine or None:
        try:
            return self._qml_engine
        except:
            return None

    @qml_application_engine.setter
    def qml_application_engine(self, qml_app_engine: QQmlApplicationEngine) -> None:
        self._qml_engine = qml_app_engine

    def get_qml_object(self, obj_name:typing.AnyStr = "") -> QObject or None:
        if obj_name != "":
            