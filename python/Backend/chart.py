
import typing
from PySide2.QtCore import QObject, Slot, Signal, Property, QTimer, QRectF
from PySide2.QtCharts import QtCharts

class ChartSignals:
    
    new_graph = Signal(str, int)
    
    scrollRight = Signal(int)


class Chart(ChartSignals):

    def __init__(self) -> None:
        self.__graph_list = {}
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.loop)
        self.__timer.start(1000)
        self.__m_x =  9
        self.__m_y = 0
        self.__xPoint =  0.0
        self.__yPoint =  0.0
                
        

    @Slot(str,QObject, result= bool)
    def add_graph(self ,name: str, graph: QtCharts.QLineSeries):
        if not name in self.__graph_list:
            self.__graph_list["name"] = graph
            return True
        else:
            return False
    @Slot(QObject)
    def set_chart(self, chart: QtCharts.QChart):
        self.__chart = chart


    @Property(QRectF)
    def plot_area(self) -> QRectF:
        try:
            return self.__plot_area
        except:
            return QRectF()
    
    @plot_area.setter
    def plot_area(self, area:QRectF):
        self.__plot_area = area

    @Property(QtCharts.QValueAxis)
    def xAxis(self) -> QtCharts.QValueAxis:
        try:
            return self.__xAxis
        except:
            return QtCharts.QValueAxis()

    @xAxis.setter
    def xAxis(self, new_x_axis: QtCharts.QValueAxis):
        self.__xAxis = new_x_axis

    @Property(QtCharts.QValueAxis)
    def yAxis(self) -> QtCharts.QValueAxis:
        try:
            return self.__yAxis
        except:
            return QtCharts.QValueAxis()

    @yAxis.setter
    def yAxis(self, new_y_axis: QtCharts.QValueAxis):
        self.__yAxis = new_y_axis



    @Slot(str,QObject, result= bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple ):
        pass

    def loop(self):
        pass

    def setup(self, dict: typing.Dict):
        pass
