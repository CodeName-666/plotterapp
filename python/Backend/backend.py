# This Python file uses the following encoding: utf-8
import hashlib
import json
from functools import partial
from typing import Any, Dict, List

from PySide6.QtCore import QObject, Slot, Signal, QTimer, QJsonValue
from PySide6.QtQml import QJSValue
from PySide6 import QtCharts

from Receiver.receiver import Receiver
from Receiver.registry import ReceiverRegistry, parse_interface_definitions
from Common.converter import Converter

# Backend interfaces
from .settings import Settings
from .serial_port import SerialPort
from .setup import Setup
from Logger import logger
from Logger.logger import Logger
from .chart import Chart


class Backend(Settings, Logger, SerialPort, Setup, Chart):

    __backend_instance = None

    def __init__(self):
        if Backend.__backend_instance != None:
            pass
        else:
            Settings.__init__(self)
            Logger.__init__(self)
            SerialPort.__init__(self)
            Setup.__init__(self)
            Chart.__init__(self)
            self.receiver_list: Dict[str, Receiver] = {}
            self.__receiver_registry = ReceiverRegistry()
            self.__interfaces_config = {}
            self._backend_events: QObject | None = None
            self._ui_handle: QObject | None = None
            self._graph_state: Dict[str, Dict[str, Any]] = {}
            self._pending_events: Dict[str, List[tuple]] = {}
            self._connected_receivers: set[str] = set()
            Backend.__backend_instance = self
            self.ui_setup.connect(self._on_ui_setup_signal)
            self.com_port_update.connect(self._forward_com_port_update)

    @staticmethod
    def get_instance():
        if Backend.__backend_instance == None:
            Backend()
        return Backend.__backend_instance

    def connect_signals(self):
        self.backend_setup_done_changed.connect(self.on_backend_setup_done)

    @Slot('str', result='bool')
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

    def config(self, config: dict):
        if not config:
            logger.log_error("Backend configuration missing")
            return

        Setup.ui_config = config.get("qml", {})
        self.__interfaces_config = parse_interface_definitions(
            config.get("interfaces", [])
        )
        self._graph_state.clear()
        self._connected_receivers.clear()
        self.receiver_list = self.__receiver_registry.create_receivers(
            self.__interfaces_config.values()
        )
        self._connect_receivers()

        logger.log_info(
            "Backend registered %s receiver(s)",
            len(self.receiver_list.keys()),
        )
        self.backend_setup_done = True

    @Slot('QString', 'QJSValue', result='bool')
    def set_settings(self, interface: str, settings: QJSValue) -> bool:
        Settings.set_settings(self, interface, settings)
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

    @Slot(result='QVariant')
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
            interface,
            {"color": self._color_from_name(interface), "index": 0, "announced": False},
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
