
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property
import typing
from Logger import logger



class Setup():

    ui_setup = Signal(dict)
    ui_setup_done_changed = Signal(bool)
    backendSetupDoneChanged = Signal(bool)

    def __init__(self) -> None:
        self.ui_config = None
        self.backend_setup_done = False
        self.ui_setup_done = False
        
    @Property(bool)
    def backend_setup_done(self) -> bool:
        try: 
            return self.__backend_setup_done
        except:
            return False

    @backend_setup_done.setter
    def backend_setup_done(self, status: bool):
        if(self.backend_setup_done != status):
            logger.info("Backend Setup Status: {}".format(status))
            self.__backend_setup_done = status
            self.backendSetupDoneChanged.emit(status)
            

    @Property(bool)
    def ui_setup_done(self) -> bool:
        try: 
            return self.__ui_setup_done
        except:
            return False

    @ui_setup_done.setter
    def ui_setup_done(self, status: bool):
        if(self.ui_setup_done != status):
            logger.info("UI Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.ui_setup_done_changed.emit(status)
    
    @property
    def ui_config(self) -> dict:
        try:
            return self.__config
        except:
            return None
    
    @ui_config.setter
    def ui_config(self, new_config: dict):
        self.__config = new_config


