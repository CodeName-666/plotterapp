
from receiver_thread import ReceiverThread
import paho.mqtt.client as mqtt
from typing import Dict


class MqttConnection(ReceiverThread):
    def __init__(self, host, port, rx_topic, tx_topic):
        ReceiverThread.__init__(self)
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
        if not self._pause:
            self.new_data.emit(msg.payload.decode())
        else:
            pass

    def send_response(self, response):
        self.client.publish(self.tx_topic, response)

    def stop_event(self):
        self.stop_event.set()
        self.client.disconnect()
    
    def connect(self):
        pass

    def disconnect(self):
        pass

    def connected(self): 
        pass

    def config(self, config: Dict):
        pass