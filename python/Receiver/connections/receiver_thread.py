from PySide6.QtCore import QThread, Signal
from typing import Optional


class ReceiverThread(QThread):

    new_data_available = Signal(bytes)

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__(parent)
        self._stop: bool = False
        self._pause: bool = False