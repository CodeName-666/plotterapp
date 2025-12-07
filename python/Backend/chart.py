"""Backend-side chart bookkeeping for graph registration and data buffering."""

from __future__ import annotations

import typing
from dataclasses import dataclass, field

from PySide6.QtCore import QObject, Slot, Signal, Property, QTimer, QRectF
from PySide6 import QtCharts


@dataclass
class _GraphBuffer:
    series: typing.Optional[QtCharts.QLineSeries] = None
    pending_points: typing.List[typing.Tuple[float, float]] = field(default_factory=list)


class Chart(QObject):

    new_graph = Signal(str, int)
    append_graph_point_signal = Signal(str, float, float)
    scrollRight = Signal(int)

    def __init__(self) -> None:
        self.__graph_list: typing.Dict[str, _GraphBuffer] = {}
        self.__chart: typing.Optional[QtCharts.QChart] = None
        self.__plot_area = QRectF()
        self.__xAxis: typing.Optional[QtCharts.QValueAxis] = None
        self.__yAxis: typing.Optional[QtCharts.QValueAxis] = None
        self.__xPoint = 0.0
        self.__scroll_step = 5
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.loop)
        self.__timer.start(1000)

    @Slot(str, QObject, result=bool)
    def add_graph(self, name: str, graph: QtCharts.QLineSeries):
        if name not in self.__graph_list:
            self.__graph_list[name] = _GraphBuffer(series=graph)
        buffer = self.__graph_list[name]
        buffer.series = graph
        if buffer.pending_points:
            for x_val, y_val in buffer.pending_points:
                buffer.series.append(x_val, y_val)
            buffer.pending_points.clear()
        return True

    @Slot(QObject)
    def set_chart(self, chart: QtCharts.QChart):
        self.__chart = chart

    @Property(QRectF)
    def plot_area(self) -> QRectF:
        return self.__plot_area

    @plot_area.setter
    def plot_area(self, area: QRectF):
        self.__plot_area = area

    @Property(QtCharts.QValueAxis)
    def xAxis(self) -> QtCharts.QValueAxis:
        return self.__xAxis if self.__xAxis else QtCharts.QValueAxis()

    @xAxis.setter
    def xAxis(self, new_x_axis: QtCharts.QValueAxis):
        self.__xAxis = new_x_axis

    @Property(QtCharts.QValueAxis)
    def yAxis(self) -> QtCharts.QValueAxis:
        return self.__yAxis if self.__yAxis else QtCharts.QValueAxis()

    @yAxis.setter
    def yAxis(self, new_y_axis: QtCharts.QValueAxis):
        self.__yAxis = new_y_axis

    def register_graph(self, name: str, color: int) -> None:
        if name not in self.__graph_list:
            self.__graph_list[name] = _GraphBuffer()
        self.new_graph.emit(name, color)

    def append_point(self, name: str, x: float, y: float) -> None:
        buffer = self.__graph_list.setdefault(name, _GraphBuffer())
        if buffer.series:
            buffer.series.append(x, y)
        else:
            buffer.pending_points.append((x, y))
        self.append_graph_point_signal.emit(name, x, y)

    @Slot(str, QObject, result=bool)
    def append_graph_point(self, graph_name: str, point: typing.Tuple):
        if not point:
            return False
        buffer = self.__graph_list.get(graph_name)
        if buffer is None or buffer.series is None:
            return False
        try:
            x_val, y_val = point
        except (ValueError, TypeError):
            return False
        buffer.series.append(x_val, y_val)
        return True

    def loop(self):
        if self.__chart is None:
            return
        self.__xPoint += self.__scroll_step
        self.scrollRight.emit(self.__scroll_step)

    def config(self, config: typing.Dict):
        if config is None:
            return
        self.__scroll_step = config.get("scroll_step", self.__scroll_step)
