# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
from Logger import logger
import typing


class Settings(QObject):

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        super(Settings,self).__init__()


    @Slot('QJSValue', result='bool')
    def set_settings(self, settings: QJSValue) -> bool:
        if settings.hasProperty("type"):
            ok = False
            for r in self.receiver_list.values():
                logger.inof("Receiver: {} == {}".format(r.type.name, settings.property("type").toString()))
                if r.type.name == settings.property("type").toString():
                    r.update_settings(settings)
                    ok = True
                    break
            if ok:
                logger.info("Settings Updated")
                return True
            else:
                logger.warning("Correct Receiver not found")
                return False
        else:
            logger.error("Config parameter TYPE not found")
            return False


    @Slot('str', result='bool')
    def settings_valid(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            return self.receiver_list[connection_type].settings_valid()
        else:
            return False