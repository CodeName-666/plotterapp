# Receiver Interface Contract

This document describes the mandatory API that every backend receiver must
implement. The goal is to keep all connection types interchangeable so the
backend can configure and start them uniformly.

## Base Class

All receivers inherit from `Receiver` (`python/Receiver/receiver.py`). The base
class already provides several helpers:

- Lifecycle orchestration that validates settings, opens the connection and
  starts/stops the worker thread.
- Signal plumbing that relays the worker thread's `new_data` signal to a
  backend facing `Receiver.new_data` signal.
- Config storage plus `_on_config_updated()` hook for subclasses.

### Signals

- `new_data: Signal(bytes)` — emitted whenever bytes are received from the
  worker thread. Backend modules should connect to this signal instead of the
  transport specific ones.

### Lifecycle Methods

- `start()` — checks `settings_valid()`, calls `open_connection()` as needed and
  starts the attached `ReceiverThread`. Raise a `ValueError` when settings are
  invalid and `ConnectionError` when the connection cannot be opened.
- `stop()` — stops the worker thread (via `stop_event`) and calls
  `close_connection()` when currently connected.

### Connection Methods (must be provided by subclasses)

- `open_connection() -> bool` — establish the transport specific connection.
  Set the connected state via `_set_connected(True)` on success and return
  `True`. Return `False` and leave the state untouched when the connection
  cannot be established.
- `close_connection() -> None` — close sockets/ports/etc. Always call
  `_set_connected(False)` before returning.
- `is_connected() -> bool` — available through the base class. Subclasses only
  need to update the state via `_set_connected()`.

### Settings and Configuration

- `settings_valid() -> bool` — validate the latest UI/backend settings. The
  backend calls this before attempting to `open_connection()`.
- `config(config_dict: Dict[str, Any])` — store backend provided configuration
  (`interfaces` entry, UI mapping, …). Override `_on_config_updated()` when
  additional processing is required.

### Thread Interaction

- `attach_thread(receiver_thread: ReceiverThread)` — call this from the
  subclass constructor when a concrete worker thread instance exists. It wires
  the worker's `new_data` signal to the receiver facing one.
- `send_response(response: bytes)` — forwards responses to the worker thread,
  provided the thread implements `send_response()`.

## Implementation Checklist

1. Define the worker thread that emits `ReceiverThread.new_data` whenever new
   bytes arrive.
2. Implement a subclass of `Receiver` and attach the thread instance via
   `attach_thread()`.
3. Validate UI settings inside `settings_valid()`.
4. Establish and tear down resources in `open_connection()`/`close_connection()`
   and keep the `_set_connected()` state in sync.
5. Emit structured payload on `new_data` or convert to protocol specific
   objects before emitting, depending on backend expectations.

Following this contract ensures any receiver can be registered in the backend
without additional glue code.
