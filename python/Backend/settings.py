# This Python file uses the following encoding: utf-8
from hashlib import new
from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer
from PySide6.QtQml import QJSValue
from Logger import logger
from typing import Optional


class Settings(QObject):

    new_interface = Signal(str)
    new_settings = Signal('QJSValue')

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super(Settings, self).__init__(parent)
        self.__settings = QJSValue()
        self.__interface = ""

    @Property(str, notify= new_interface)
    def interface(self) -> str:
        return self.__interface

    @interface.setter
    def interface(self,new_interface: str):
        if self.__interface != new_interface:
            self.__interface = new_interface
            self.new_interface.emit(new_interface)
            logger.log_debug("New Interface: {}".format(new_interface))

    @Property('QJSValue', notify= new_settings)
    def settings(self) -> QJSValue:
        return self.__settings       
    
    @settings.setter
    def settings(self,new_settings: QJSValue):
        if self.__settings != new_settings:
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
