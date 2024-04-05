
from receiver_thread import ReceiverThread
import paho.mqtt.client as mqtt
from typing import Dict


class MqttConnection(ReceiverThread):
    def __init__(self, host, port, rx_topic, tx_topic):
        ReceiverThread.__init__(self)
        self.__host = host
        self.__port = port
        self.__rx_topic = rx_topic
        self.__tx_topic = tx_topic

        self.__client = mqtt.Client()
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message
        

    def run(self):
        self.__client.connect(self.__host, self.__port)
        self.__client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.__client.subscribe(self.__rx_topic)

    def on_message(self, client, userdata, msg):
        self.new_data.emit(msg.payload.decode())

    def send_response(self, response):
        self.__client.publish(self.__tx_topic, response)

    def stop(self):
        self.__client.disconnect()
    
    def connect(self):
        pass

    def disconnect(self):
        pass

    def connected(self): 
        pass

    def config(self, config: Dict):
        pass