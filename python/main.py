# This Python file uses the following encoding: utf-8
import sys
import os
import sys
import json
from os.path import abspath, dirname, join

from PySide2.QtQml import QQmlDebuggingEnabler
from PySide2.QtCore import QObject, Slot

from plotter import Plotter

from backend import Backend
from serial_connection import SerialConnection, SerialConfig
from telnet_connection import TelnetConnection




# from style_rc import *

def getJsonConfigData(json_path : str):
    file_path = os.path.dirname(__file__)
    if file_path:
        config = file_path + '/' + json_path
    else:
        config = json_path
    try:
        with open(config) as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None

def getInterface(json_config: dict, type: str):
    if json_config:
        interface_list = json_config["interfaces"]
        for interface in interface_list:
            if interface["type"] == type:
                return interface
        return None

def getSerialConfig(json_config: dict):
    return getInterface(json_config,"Serial")
        

def getTelnetConfig(json_config: dict):
    return getInterface(json_config,"Telnet")



if __name__ == "__main__":

    # QQmlDebuggingEnabler()
    json_config = getJsonConfigData('../config/config.json')
    serial_config = getSerialConfig(json_config)
    telnet_config = getTelnetConfig(json_config)

    # Instance of the Python object
    serial = SerialConnection(serial_config["default"])
    telnet = TelnetConnection(telnet_config["default"])

    plotter = Plotter(sys.argv,json_config)
    backend = Backend()       

    backend.add_receiver(telnet_config["type"], telnet)
    backend.add_receiver(serial_config["type"], serial)

    plotter.set_backend(backend)
    plotter.setup_app()
    

    if not plotter.rootObjects():
        sys.exit(-1)

    sys.exit(plotter.run())
