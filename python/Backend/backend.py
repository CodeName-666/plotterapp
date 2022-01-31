# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, Slot, Signal, QTimer
from PySide2.QtQml import QJSValue
from receiver import Receiver, ConnectionType


class Backend(QObject):

    def __init__(self):
        super(Backend, self).__init__()
        self._receiver_list = dict()
        self._receiver = None

    @property
    def receiver(self, new_receiver):
        self._receiver = new_receiver

    @receiver.setter
    def receiver(self):
        return self._receiver

    @property
    def receiver_list(self):
        return self._receiver_list

    def add_receiver(self, key: str, receiver: Receiver):
        if receiver is not None:
            self.receiver_list[key] = receiver

    def get_config(self, connection_type: str):
        receiver = self.receiver_list
        if connection_type in receiver.keys():
            return self.receiver_list[connection_type].config
        else:
            return None

    @Slot(result=list)
    def get_com_ports(self) -> list:
        return self.receiver_list["SERIAL"].settings.com_list

    @Slot('QJSValue', result='bool')
    def set_settings(self, settings: QJSValue) -> bool:
        if settings.hasProperty("type"):
            ok = False
            for r in self.receiver_list.values():
                print("Receiver: {} == {}".format(r.type.name, settings.property("type").toString()))
                if r.type.name == settings.property("type").toString():
                    r.update_settings(settings)
                    ok = True
                    break
            if ok:
                print("Settings Updated")
                return True
            else:
                print("Correct Receiver not found")
                return False
        else:
            print("Config parameter TYPE not found")
            return False

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
