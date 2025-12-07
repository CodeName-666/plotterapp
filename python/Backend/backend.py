# This Python file uses the following encoding: utf-8
import hashlib
import json
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Dict, List, Optional, Tuple

from PySide6 import QtCharts
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QJsonValue, Property, QRectF
from PySide6.QtQml import QJSValue
from serial.tools import list_ports

from Receiver.receiver import Receiver
from Receiver.registry import ReceiverRegistry, parse_interface_definitions
from Common.converter import Converter
from Logger import logger
from Logger.logger import Logger


def _get_serial_ports() -> List[str]:
    ports = list_ports.comports()
    return [port.name for port in ports]


@dataclass
class _GraphBuffer:
    series: Optional[QtCharts.QLineSeries] = None
    pending_points: List[Tuple[float, float]] = field(default_factory=list)


class Backend(QObject):
    """Single QObject-based backend used by QML."""

    __backend_instance: Optional["Backend"] = None

    # Settings signals
    new_interface = Signal(str)
    new_settings = Signal("QJSValue")

    # Setup/connection signals
    ui_setup = Signal("QVariant")
    ui_setup_done_changed = Signal(bool)
    backend_setup_done_changed = Signal(bool)

    # Serial-port discovery
    com_port_update = Signal("QVariant")

    def __init__(self) -> None:
        super().__init__()
        if Backend.__backend_instance is not None:
            raise RuntimeError("Backend already initialized")

        # Settings state
        self.__settings = QJSValue()
        self.__interface = ""

        # Setup state
        self.ui_config: Dict[str, Any] | None = None
        self.__ui_setup_done = False
        self.__backend_setup_done = False

        # Receiver/graph bookkeeping
        self.receiver_list: Dict[str, Receiver] = {}
        self.__receiver_registry = ReceiverRegistry()
        self.__interfaces_config: Dict[str, Any] = {}
        self._backend_events: QObject | None = None
        self._ui_handle: QObject | None = None
        self._graph_state: Dict[str, Dict[str, Any]] = {}
        self._pending_events: Dict[str, List[tuple]] = {}
        self._connected_receivers: set[str] = set()

        # Chart helpers
        self.__graph_list: Dict[str, _GraphBuffer] = {}
        self.__plot_area = QRectF()
        self.__chart: Optional[QtCharts.QChart] = None
        self.__xAxis: Optional[QtCharts.QValueAxis] = None
        self.__yAxis: Optional[QtCharts.QValueAxis] = None
        self.__xPoint = 0.0
        self.__scroll_step = 5

        # Serial port polling
        self.__com_updater_timer = QTimer(self)
        self.__com_list: List[str] = []
        self.__com_updater_timer.timeout.connect(self._update_com_ports)
        self.__com_updater_timer.start(1000)

        # Auto-scroll timer for charts
        self.__scroll_timer = QTimer(self)
        self.__scroll_timer.timeout.connect(self._on_scroll_timer)
        self.__scroll_timer.start(1000)

        # Signal wiring to forward into QML event bridge
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)
        self.ui_setup.connect(self._on_ui_setup_signal)
        self.com_port_update.connect(self._forward_com_port_update)

        Backend.__backend_instance = self

    @staticmethod
    def get_instance() -> "Backend":
        if Backend.__backend_instance is None:
            Backend()
        return Backend.__backend_instance  # type: ignore[return-value]

    # ------------------------------------------------------------------ #
    # Properties exposed to QML
    # ------------------------------------------------------------------ #
    @Property(str, notify=new_interface)
    def interface(self) -> str:
        return self.__interface

    @interface.setter
    def interface(self, new_interface: str) -> None:
        if self.__interface != new_interface:
            self.__interface = new_interface
            self.new_interface.emit(new_interface)
            logger.log_debug("New Interface: {}".format(new_interface))

    @Property("QJSValue", notify=new_settings)
    def settings(self) -> QJSValue:
        return self.__settings

    @settings.setter
    def settings(self, new_settings: QJSValue) -> None:
        if self.__settings != new_settings:
            self.__settings = new_settings
            logger.log_debug("New Settings")
            self.new_settings.emit(new_settings)

    @Property(bool, notify=backend_setup_done_changed)
    def backend_setup_done(self) -> bool:
        return self.__backend_setup_done

    @backend_setup_done.setter
    def backend_setup_done(self, status: bool) -> None:
        if self.__backend_setup_done != status:
            logger.log_info("Backend Setup Status: {}".format(status))
            self.__backend_setup_done = status
            self.backend_setup_done_changed.emit(status)

    @Property(bool, notify=ui_setup_done_changed)
    def ui_setup_done(self) -> bool:
        return self.__ui_setup_done

    @ui_setup_done.setter
    def ui_setup_done(self, status: bool) -> None:
        if self.__ui_setup_done != status:
            logger.log_info("UI Setup Status: {}".format(status))
            self.__ui_setup_done = status
            self.ui_setup_done_changed.emit(status)

    @Property(QRectF)
    def plot_area(self) -> QRectF:
        return self.__plot_area

    @plot_area.setter
    def plot_area(self, area: QRectF) -> None:
        self.__plot_area = area

    @Property(QObject)
    def xAxis(self) -> QtCharts.QValueAxis:
        """Expose the X axis as QObject to keep the meta type valid."""
        return self.__xAxis if self.__xAxis else QtCharts.QValueAxis()

    @xAxis.setter
    def xAxis(self, new_x_axis: QObject) -> None:
        self.__xAxis = new_x_axis if isinstance(new_x_axis, QtCharts.QValueAxis) else None

    @Property(QObject)
    def yAxis(self) -> QtCharts.QValueAxis:
        """Expose the Y axis as QObject to keep the meta type valid."""
        return self.__yAxis if self.__yAxis else QtCharts.QValueAxis()

    @yAxis.setter
    def yAxis(self, new_y_axis: QObject) -> None:
        self.__yAxis = new_y_axis if isinstance(new_y_axis, QtCharts.QValueAxis) else None

    # ------------------------------------------------------------------ #
    # Public API used from QML/receivers
    # ------------------------------------------------------------------ #
    def connect_signals(self) -> None:
        """Kept for backward compatibility."""
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)

    @Slot(str, result="bool")
    def connectTo(self, connection_type: str) -> bool:
        receiver = self.receiver_list.get(connection_type)
        if receiver is None:
            self._notify_status("error", f"Invalid connection type: {connection_type}")
            return False

        try:
            receiver.start()
        except ValueError as exc:
            self._notify_status("warning", f"Receiver settings invalid: {exc}")
            return False
        except ConnectionError as exc:
            self._notify_status("error", f"Unable to open receiver connection: {exc}")
            return False

        self._notify_status("info", f"Receiver {connection_type} started")
        return True

    def config(self, config: dict) -> None:
        if not config:
            logger.log_error("Backend configuration missing")
            return

        self.ui_config = config.get("qml", {})
        self.__interfaces_config = parse_interface_definitions(config.get("interfaces", []))
        self.__scroll_step = config.get("scroll_step", self.__scroll_step)
        self._graph_state.clear()
        self._connected_receivers.clear()
        self.receiver_list = self.__receiver_registry.create_receivers(self.__interfaces_config.values())
        self._connect_receivers()

        logger.log_info("Backend registered %s receiver(s)", len(self.receiver_list.keys()))
        self.backend_setup_done = True

    @Slot("QString", "QJSValue", result="bool")
    def set_settings(self, interface: str, settings: QJSValue) -> bool:
        self.interface = interface
        self.settings = settings

        receiver = self.receiver_list.get(interface)
        if receiver is None:
            self._notify_status("warning", f"Unknown interface for settings: {interface}")
            return False

        py_settings = Converter.jsvalue_to_dict(settings)
        if not isinstance(py_settings, dict):
            self._notify_status("warning", f"Cannot convert settings for {interface}")
            return False

        receiver.config(py_settings)
        self._notify_status("info", f"Updated settings for {interface}")
        return True

    @Slot(str, result="bool")
    def settings_valid(self, connection_type: str) -> bool:
        if connection_type in self.receiver_list.keys():
            return self.receiver_list[connection_type].settings_valid()
        return False

    @Slot(result="QVariant")
    def get_ui_config(self):
        try:
            return self.ui_config
        except AttributeError:
            return {}

    @Slot(QObject, QObject)
    def setup(self, ui_handle: QObject, backend_events: QObject) -> None:
        self._ui_handle = ui_handle
        self._backend_events = backend_events
        logger.log_info("Backend connected to QML events bridge")
        self._flush_pending_events()

    # Logging slots for QML use
    @Slot(str)
    def log_error(self, msg: str) -> None:
        Logger.get_instance().log_error(msg)

    @Slot(str)
    def log_warning(self, msg: str) -> None:
        Logger.get_instance().log_warning(msg)

    @Slot(str)
    def log_info(self, msg: str) -> None:
        Logger.get_instance().log_info(msg)

    @Slot(str)
    def log_debug(self, msg: str) -> None:
        Logger.get_instance().log_debug(msg)

    @Slot(str)
    def log_stack(self, stack_info: str) -> None:
        Logger.get_instance().log_qml_stack(stack_info)

    # Chart helpers used from QML
    @Slot(str, QObject, result=bool)
    def add_graph(self, name: str, graph: QtCharts.QLineSeries) -> bool:
        buffer = self.__graph_list.setdefault(name, _GraphBuffer())
        buffer.series = graph
        if buffer.pending_points:
            for x_val, y_val in buffer.pending_points:
                buffer.series.append(x_val, y_val)
            buffer.pending_points.clear()
        return True

    @Slot(QObject)
    def set_chart(self, chart: QtCharts.QChart) -> None:
        self.__chart = chart

    @Slot(QRectF)
    def set_plot_area(self, area: QRectF) -> None:
        self.plot_area = area

    @Slot(QObject, QObject)
    def set_axis(self, x_axis: QObject, y_axis: QObject) -> None:
        self.xAxis = x_axis
        self.yAxis = y_axis

    @Slot(str, QObject, result=bool)
    def append_graph_point(self, graph_name: str, point: Tuple) -> bool:
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

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _connect_receivers(self) -> None:
        for name, receiver in self.receiver_list.items():
            if name in self._connected_receivers:
                continue
            receiver.new_data.connect(partial(self._on_receiver_data, name))
            self._connected_receivers.add(name)

    def _on_receiver_data(self, interface: str, payload: bytes) -> None:
        value = self._extract_numeric_value(interface, payload)
        if value is None:
            return

        state = self._graph_state.setdefault(
            interface, {"color": self._color_from_name(interface), "index": 0, "announced": False}
        )

        if not state["announced"]:
            self._queue_event("newGraph", interface, state["color"])
            state["announced"] = True

        point = {"x": state["index"], "y": value}
        state["index"] += 1
        self._queue_event("append_graph_point", interface, point)

    def _extract_numeric_value(self, interface: str, payload: bytes) -> float | None:
        if not payload:
            return None

        try:
            text = payload.decode("utf-8").strip()
        except UnicodeDecodeError:
            self._notify_status("warning", f"{interface}: received non-text payload")
            return None

        if not text:
            return None

        try:
            return float(text)
        except ValueError:
            pass

        try:
            decoded = json.loads(text)
        except json.JSONDecodeError:
            self._notify_status("warning", f"{interface}: cannot parse payload '{text[:40]}...'")
            return None

        if isinstance(decoded, (int, float)):
            return float(decoded)

        if isinstance(decoded, dict):
            candidate = decoded.get("payload")
            if isinstance(candidate, (int, float)):
                return float(candidate)
            if isinstance(candidate, str):
                try:
                    return float(candidate)
                except ValueError:
                    self._notify_status("warning", f"{interface}: payload missing numeric value")
                    return None

        return None

    def _color_from_name(self, name: str) -> int:
        digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
        return int(digest[:6], 16)

    def _on_ui_setup_signal(self, settings: dict) -> None:
        self._queue_event("ui_setup", settings)

    def _forward_com_port_update(self, ports) -> None:
        self._queue_event("com_port_update", ports)

    def _on_scroll_timer(self) -> None:
        if self._backend_events is None:
            return
        self.__xPoint += self.__scroll_step
        self._queue_event("scrollRight", self.__scroll_step)

    def _queue_event(self, signal_name: str, *args) -> None:
        if self._emit_event(signal_name, *args):
            return
        self._pending_events.setdefault(signal_name, []).append(args)

    def _emit_event(self, signal_name: str, *args) -> bool:
        if self._backend_events is None:
            return False
        signal = getattr(self._backend_events, signal_name, None)
        if signal is None or not hasattr(signal, "emit"):
            return False
        signal.emit(*args)
        return True

    def _flush_pending_events(self) -> None:
        if self._backend_events is None:
            return
        for signal_name, events in list(self._pending_events.items()):
            for args in events:
                self._emit_event(signal_name, *args)
        self._pending_events.clear()

    def _notify_status(self, level: str, message: str) -> None:
        level = level.lower()
        if level == "error":
            logger.log_error(message)
        elif level == "warning":
            logger.log_warning(message)
        elif level == "debug":
            logger.log_debug(message)
        else:
            logger.log_info(message)

        self._queue_event("status_message", level, message)

    # Setup when backend is ready
    def on_backend_setup_done(self, status: bool) -> None:
        if status:
            if not self.ui_setup_done and self.ui_config is not None:
                self.ui_setup.emit(self.ui_config)
            else:
                logger.log_info("UI already configured")
        else:
            logger.log_error("Cannot setup ui. Backend not configured")

    # Serial port polling callback
    def _update_com_ports(self) -> None:
        new_com_list = _get_serial_ports()
        if new_com_list != self.__com_list:
            logger.log_info("New Comports found {}".format(new_com_list))
            self.com_port_update.emit(new_com_list)
            self.__com_list = new_com_list
