
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property
import typing
from Logger import logger


class Setup():

    setup_ui = Signal(dict)
    setup_ui_done_changed = Signal(bool)
    setup_backend_done_changed = Signal(bool)

    def __init__(self) -> None:
        self.ui_config = None
        self.setup_backend_done = False
        self.setup_ui_done = False
        #self.setup_backend_done_changed.connect(self.on_backend_setup_done)
        
    @Property(bool)
    def setup_backend_done(self) -> bool:
        try: 
            return self.__backend_setup_done
        except:
            return False

    @setup_backend_done.setter
    def setup_backend_done(self, status: bool):
        if(self.setup_backend_done != status):
            logger.info("Backend Setup Status: {}".format(status))
            self.__backend_setup_done = status
            self.setup_backend_done_changed.emit(status)
            

    @Property(bool)
    def setup_ui_done(self) -> bool:
        try: 
            return self.__ui_setup_done
        except:
            return False

    @setup_ui_done.setter
    def setup_ui_done(self, status: bool):
        if(self.setup_ui_done != status):
            logger.info("UI Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.setup_ui_done_changed.emit(status)
    
    def on_backend_setup_done(self, status: bool):
        if status:
            if not self.setup_ui_done:
                self.setup_ui.emit(self.ui_config)
            else:
                logger.info("UI already configured")
        else:
            logger.error("Cannot setup ui. Backend not configured")


    @property
    def ui_config(self) -> dict:
        try:
            return self.__config
        except:
            return None
    
    @ui_config.setter
    def ui_config(self, new_config: dict):
        self.__config = new_config


