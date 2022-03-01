
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer, Property
import typing
from Logger import logger



class Setup():
    backend_setup_done_changed = Signal()
    ui_setup = Signal(dict)
    ui_setup_done_changed = Signal()


    def __init__(self) -> None:
        self.backend_setup_done = False
        self.ui_setup_done = False
        self.ui_config = None

    @Property(bool, notify=backend_setup_done_changed)
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
            self.backend_setup_done_changed.emit()
            

    @Property(bool, notify=ui_setup_done_changed)
    def ui_setup_done(self) -> bool:
        try: 
            return self.__ui_setup_done
        except:
            return False


    def ui_setup_done(self, status: bool):
        if(self.__ui_setup_done != status):
            logger.info("Backend Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.ui_setup_done_changed.emit()
    
    @property(dict)
    def ui_config(self) -> typing.Dict:
        try:
            return self.__config
        except:
            return None
    
    @ui_config.setter
    def ui_config(self, new_config: typing.Dict):
        self.__config = new_config
