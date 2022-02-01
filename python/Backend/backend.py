# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
from Receiver.receiver import Receiver, ConnectionType
from python.Receiver import receiver
from settings import Settings


class Backend(Settings):

    def __init__(self):
        super(Settings, self).__init__()


    @property
    def receiver(self):
        try:
            return self._receiver
        except:
            return None
    
    @receiver.setter
    def receiver(self, receiver: Receiver) -> int:
        self._receiver = receiver


    @Slot('str', result='bool')
    def connect(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            if self.receiver_list[connection_type].settings_valid():
                if not self.receiver_list[connection_type].is_connected():
                    if self.receiver_list[connection_type].open_connection():
                        return True
                    else:
                        print("Cannot open connection, undef error")
                        return False
                else:
                    print("Allready Connected")
                    return False
            else:
                print("Invalid settings")
                return False
        else:
            print("Invalid Connection type")
            return False

    @Slot('str', result='bool')
    def settings_valid(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            return self.receiver_list[connection_type].settings_valid()
        else:
            return False
