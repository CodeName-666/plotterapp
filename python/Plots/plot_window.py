
import typing
from PySide2 import QtCore
from PySide2.QtWidgets import QWidget
from PySide2.QtCharts import QtCharts


class PlotWindow(QtCharts.QChart):

    #def __init__(self, type:QtCharts.QChart.ChartType, parent: QGraphicsItem = None, wFlags: QtCore.Qt.WindowFlags = QtCore.Qt.Window) -> None:
    #    super().__init__(type, parent, wFlags)
    #    self.setTitle("TEST CHART")
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)
        self.setTitle("TEST")
        