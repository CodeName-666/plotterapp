
import typing
from PySide2.QtCore import QObject, Slot, Signal, Property, QTimer, QRectF
from PySide2.QtCharts import QtCharts


class Chart():

    new_graph = Signal(str, int)
    scroll = Signal(int)

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

    @Slot(str,QObject, result= bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple ):
        pass

    def loop(self):
        pass

    def setup(self, dict: typing.Dict):
        pass
