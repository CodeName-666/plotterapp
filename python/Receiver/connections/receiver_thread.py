from PySide6.QtCore import QThread, Signal, Slot
from typing import Optional


class ReceiverThread(QThread):

    new_data = Signal(bytes)
    

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__(parent)
        self._stop: bool = False
        self._data: list = []
        

    def add_new_data(self, data: bytes):
        self._data.append(data)

    def get_data(self):
        return self._data

    def stop(self):
        self._stop = True

    @Slot()
    def on_stop(self):
        pass
