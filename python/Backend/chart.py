
import re
import typing
from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts


class Chart():

    new_graph = Signal(str, int)

    def __init__(self) -> None:
        self._graph_list = []
        
        

    @Slot(str,QObject, result= bool)
    def add_graph(self ,name: str, graph: QtCharts.QLineSeries):
        if not name in self._graph_list:
            self._graph_list["name"] = graph
            return True
        else:
            return False

    @Property(QObject)
    def chart(self):
        try:
            return self._chart
        except:
            return None

    @chart.setter
    def chart(self, chart: QtCharts.QChart):
        self._chart = chart

    @Slot(str,QObject, result= bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple ):
        pass


    def setup(self, dict: typing.Dict):
        pass
