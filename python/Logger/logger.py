import logging
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
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
            Logger(None,None)
        return Logger.__instance

    @property
    def enabled(self):
        try:
            return self._enabled
        except: 
            return False

    def log_message(self, type: str, msg, *args, **kwargs):
        if(type == 'ERROR'):
            logging.error(msg,*args, **kwargs)
        elif(type == 'WARN'):
            logging.warning(msg,*args, **kwargs)
        elif(type == 'INFO'):
            logging.info(msg,*args, **kwargs)
        elif(type == 'DEBUG'):
            logging.debug(msg,*args, **kwargs)
        else:
            logging.debug(msg,*args, **kwargs)
        

    @enabled.setter
    def enabled(self, status):
        self._enabled = status   

    def setup(self, config: dict) -> None:
        self.enabled = config["enabled"]
        log_level = config["level"]
        name = config["name"]
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
    


    