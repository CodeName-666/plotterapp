import logging
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Property
import typing


def warning(msg, *args, **kwargs):
    Logger.get_instance().log_message('WARN', msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    Logger.get_instance().log_message('INFO', msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    Logger.get_instance().log_message('ERROR', msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    Logger.get_instance().log_message('DEBUG', msg, *args, **kwargs)



class Logger(QObject):
    
    __instance = None
    def __init__(self) -> None:
        if Logger.__instance != None:
            pass
        else:
            super(QObject,self).__init__()
            Logger.__instance = self

    @staticmethod
    def get_instance():
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    @Property(bool)
    def enabled(self):
        try:
            return self._enabled
        except: 
            return False
            
    @enabled.setter
    def enabled(self, status):
        self._enabled = status

    def log_message(self, type: str, msg, *args, **kwargs):
        if self.enabled: 
            if(type == 'ERROR'):
                logging.error(msg,*args, **kwargs)
            elif(type == 'WARN'):
                logging.warning(msg,*args, **kwargs)
            elif(type == 'INFO'):
                logging.info(msg,*args, **kwargs)
            elif(type == 'DEBUG'):
                logging.debug(msg,*args, **kwargs)
            else:
                logging.debug('INVALID LOG_TYPE: '.format(msg),*args, **kwargs)

    def log_qml_message(self, type: str, msg, *args, **kwargs):
        self.log_message(type, 'QML - {}'.fromat(msg), *args, **kwargs)

    @Slot(str)
    def logError(self, msg: str):
        self.get_instance().log_qml_message('ERROR',msg)
    
    @Slot(str)
    def logWarning(self, msg: str):
        self.get_instance().log_qml_message('WARN',msg)
    @Slot(str)
    def logInfo(self, msg: str):
        self.get_instance().log_qml_message('INFO',msg)
    @Slot(str)
    def logDebug(self, msg: str):
        self.get_instance().log_qml_message('DEBUG',msg)

    @enabled.setter
    def enabled(self, status):
        self._enabled = status   

    def setup(self, config: dict) -> None:
        log_config = config["logging"]
        self.enabled = log_config["enabled"]
        log_level = log_config["level"]
        name = log_config["name"]
        if self.enabled:
            logging.basicConfig(filename=name, encoding='utf-8',
                        format='%(asctime)s: %(levelname)s - %(message)s', level=log_level)

    


if __name__ == "__main__":
    config = {
        "enabled": 1,
        "name" : "logfile.log",
        "level": "DEBUG"
    }

    x = Logger()
    x.setup(config)

    warning("test 1,2,3")
    debug("laösdjflas")
    


    