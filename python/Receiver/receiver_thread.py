from PySide6.QtCore import QThread
from typing import Optional


class ReceiverThread(QThread):

    def __init__(self, parent: Optional[PySide6.QtCore.QObject] = ...) -> None:
        super().__init__(parent)