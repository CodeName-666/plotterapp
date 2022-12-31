# This Python file uses the following encoding: utf-8
from hashlib import new
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer
from PySide6.QtQml import QJSValue
from Logger import logger
import typing


class Settings(QObject):

    new_interface = Signal(str)
    new_settings = Signal('QJSValue')

    def __init__(self, parent: typing.Optional[QObject] = ...) -> None:
        super(Settings, self).__init__()

    @Property(str, notify= new_interface)
    def interface(self) -> str:
        try:
            return self.__interface
        except Exception:
            return ""

    @interface.setter
    def interface(self,new_interface: str):
        if self.interface != new_interface:
            self.__interface = new_interface
            logger.log_debug("New Interface: {}".format(new_interface))
            self.new_interface.emit(new_interface)

    @Property('QJSValue', notify= new_settings)
    def settings(self) -> QJSValue:
        try: 
            return self.__settings
        except Exception:
            return QJSValue()
    
    @settings.setter
    def settings(self,new_settings: QJSValue):
        if self.settings != new_settings:
            self.__settings = new_settings
            logger.log_debug("New Settings: ")
            self.new_settings.emit(new_settings)

    @Slot('QString','QJSValue', result='bool')
    def set_settings(self, interface: str, settings: QJSValue) -> bool:
        self.interface = interface
        self.settings = settings
        
  
    @Slot('str', result='bool')
    def settings_valid(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            return self.receiver_list[connection_type].settings_valid()
        else:
            return False
