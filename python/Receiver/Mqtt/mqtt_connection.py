
from PySide6 import QtCore
import paho.mqtt.client as mqtt


class MQTTReceiverThread(QtCore.QThread):
    def __init__(self, host, port, rx_topic, tx_topic):
        QtCore.QThread.__init__(self)
        self.host = host
        self.port = port
        self.rx_topic = rx_topic
        self.tx_topic = tx_topic

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        #self.stop_event = threading.Event()

    def run(self):
        self.client.connect(self.host, self.port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.rx_topic)

    def on_message(self, client, userdata, msg):
        self.parent.data.append(msg.payload.decode())

    def send_response(self, response):
        self.client.publish(self.tx_topic, response)

    def stop(self):
        self.stop_event.set()
        self.client.disconnect()