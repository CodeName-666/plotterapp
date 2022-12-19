import json

class CANConfig:
    def __init__(self, channel, bustype):
        self.channel = channel
        self.bustype = bustype

    def to_json(self):
        return json.dumps({"channel": self.channel, "bustype": self.bustype})

class MQTTConfig:
    def __init__(self, host, port, topic):
        self.host = host
        self.port = port
        self.topic = topic

    def to_json(self):
        return json.dumps({"host": self.host, "port": self.port, "topic": self.topic})

class TCPConfig:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def to_json(self):
        return json.dumps({"host": self.host, "port": self.port})



class SerialConfig:
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts

    def to_json(self):
        return json.dumps({
            "port": self.port,
            "baudrate": self.baudrate,
            "bytesize": self.bytesize,
            "parity": self.parity,
            "stopbits": self.stopbits,
            "timeout": self.timeout,
            "xonxoff": self.xonxoff,
            "rtscts": self.rtscts
        })

    @staticmethod
    def from_json(config_json):
        config = json.loads(config_json)
        return SerialConfig(
            port=config["port"],
            baudrate=config["baudrate"],
            bytesize=config["bytesize"],
            parity=config["parity"],
            stopbits=config["stopbits"],
            timeout=config["timeout"],
            xonxoff=config["xonxoff"],
            rtscts=config["rtscts"]
        )
