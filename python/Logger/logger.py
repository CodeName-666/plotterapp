import logging
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Property
import typing


def warning(msg, *args, **kwargs):
    Logger.get_instance().log_pyt_message('WARN', msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    Logger.get_instance().log_pyt_message('INFO', msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    Logger.get_instance().log_pyt_message('ERROR', msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    Logger.get_instance().log_pyt_message('DEBUG', msg, *args, **kwargs)


class Logger():
    
    __instance = None
    def __init__(self) -> None:
        if Logger.__instance != None:
            pass
        else:
            Logger.__instance = self

    @staticmethod
    def get_instance():
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    @Property(bool)
    def enabled(self):
        try:
            return Logger._enabled
        except: 
            return False

    @enabled.setter
    def enabled(self, status):
        Logger._enabled = status

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
            elif(type == 'STACK'):
                logging.debug(msg,*args, **kwargs)
            else:
                logging.debug('INVALID LOG_TYPE: '.format(msg),*args, **kwargs)

    def log_qml_message(self, type: str, msg, *args, **kwargs):
        self.log_message(type, 'QML - {}'.format(msg), *args, **kwargs)

    def log_pyt_message(self, type: str, msg, *args, **kwargs):
        self.log_message(type, 'PYT - {}'.format(msg), *args, **kwargs)

    @Slot(str)
    def log_error(self, msg: str):
        Logger.get_instance().log_qml_message('ERROR',msg)

    @Slot(str)
    def log_warning(self, msg: str):
        Logger.get_instance().log_qml_message('WARN',msg)

    @Slot(str)
    def log_info(self, msg: str):
        Logger.get_instance().log_qml_message('INFO',msg)

    @Slot(str)
    def log_debug(self, msg: str):
        Logger.get_instance().log_qml_message('DEBUG',msg)
    
    @Slot(str)
    def log_qml_stack(self,stack_info): 
        self.log_message("STACK", 'QML Stack - {}'.format(stack_info))

    def config(self, config: dict) -> None:
        self.enabled = config["enabled"]
        log_level = config["level"]
        name = config["name"]

        if self.enabled:
            logging.basicConfig(filename=name,
                        format='%(asctime)s: %(levelname)s - %(message)s', level=log_level)

    


if __name__ == "__main__":
    config = {
        "enabled": 1,
        "name" : "logfile.log",
        "level": "DEBUG"
    }

    x = Logger()
    x.config(config)

    warning("test 1,2,3")
    debug("laösdjflas")
    


    