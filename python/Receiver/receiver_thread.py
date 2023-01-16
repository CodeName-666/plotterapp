from PySide6.QtCore import QThread, Signal, Slot,QObject
from typing import Optional


class ReceiverThread(QThread):

    new_data = Signal(bytes)
    stop_event = Signal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super(ReceiverThread, self).__init__(parent)
        self.__stop: bool = False
        self.stop_event.connect(self.on_stop)

    def stop(self):
        pass
    
    def stopped(self):
        return self.__stop    

    @Slot()
    def on_stop(self):
        self.__stop = True
        self.stop()
