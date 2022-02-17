
import typing
from PySide2.QtCore import QObject, Slot, Signal, Property, QTimer
from PySide2.QtCharts import QtCharts


class Chart():

    new_graph = Signal(str, int)

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


    @Property(QtCharts.QChart)
    def chart(self):
        try:
            return self._chart
        except:
            return None

    @chart.setter
    def chart(self, chart: QtCharts.QChart):
        print("Set Chart: {}".format(self._chart))
        self._chart = chart

    @Slot(str,QObject, result= bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple ):
        pass

    def loop(self):
        c = self._chart
        c.axes()
        print("loop")

    def setup(self, dict: typing.Dict):
        pass
