
import typing
from PySide2.QtCore import QObject, Slot, Signal, Property, QTimer, QRectF
from PySide2.QtCharts import QtCharts

class ChartSignals:
    
    new_graph = Signal(str, int)
    
    scrollRight = Signal(int)


class Chart(ChartSignals):

    def __init__(self) -> None:
        self._graph_list = {}
        self._timer = QTimer()
        self._timer.timeout.connect(self.loop)
        self._timer.start(1000)
        self._m_x =  9
        self._m_y = 0
        self._xPoint =  0.0
        self._yPoint =  0.0
                
        

    @Slot(str,QObject, result= bool)
    def add_graph(self ,name: str, graph: QtCharts.QLineSeries):
        if not name in self._graph_list:
            self._graph_list["name"] = graph
            return True
        else:
            return False
    @Slot(QObject)
    def set_chart(self, chart: QtCharts.QChart):
        self._chart = chart


    @Property(QRectF)
    def plot_area(self) -> QRectF:
        try:
            return self._plot_area
        except:
            return QRectF()
    
    @plot_area.setter
    def plot_area(self, area:QRectF):
        self._plot_area = area

    @Property(QtCharts.QValueAxis)
    def xAxis(self) -> QtCharts.QValueAxis:
        try:
            return self._xAxis
        except:
            return QtCharts.QValueAxis()

    @xAxis.setter
    def xAxis(self, new_x_axis: QtCharts.QValueAxis):
        self._xAxis = new_x_axis

    @Property(QtCharts.QValueAxis)
    def yAxis(self) -> QtCharts.QValueAxis:
        try:
            return self._yAxis
        except:
            return QtCharts.QValueAxis()

    @yAxis.setter
    def yAxis(self, new_y_axis: QtCharts.QValueAxis):
        self._yAxis = new_y_axis



    @Slot(str,QObject, result= bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple ):
        pass

    def loop(self):
        pass

    def setup(self, dict: typing.Dict):
        pass
