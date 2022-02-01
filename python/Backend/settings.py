# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
import typing


class Settings(QObject):

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        super().__init__(parent)


    @Slot('QJSValue', result='bool')
    def set_settings(self, settings: QJSValue) -> bool:
        if settings.hasProperty("type"):
            ok = False
            for r in self.receiver_list.values():
                print("Receiver: {} == {}".format(r.type.name, settings.property("type").toString()))
                if r.type.name == settings.property("type").toString():
                    r.update_settings(settings)
                    ok = True
                    break
            if ok:
                print("Settings Updated")
                return True
            else:
                print("Correct Receiver not found")
                return False
        else:
            print("Config parameter TYPE not found")
            return False