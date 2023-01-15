from PySide6.QtCore import QThread, Signal, Slot
from typing import Optional


class ReceiverThread(QThread):

    new_data = Signal(bytes)
    stop_event = Signal()

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__(parent)
        self.__stop: bool = False

    @Slot()
    def stop_event(self):
        pass
    
    def stopped(self):
        return self.__stop    

    
    def on_stop(self):
        self.__stop = True
