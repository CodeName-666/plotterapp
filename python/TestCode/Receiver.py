import threading
import paho.mqtt.client as mqtt

class Receiver:
    def __init__(self, receiver_thread):
        self.receiver_thread = receiver_thread
        self.data = []
        self.receiver_thread.parent = self
        self.receiver_thread.start()

    def get_data(self):
        return self.data

    def send_response(self, response):
        self.receiver_thread.send_response(response)

    def stop(self):
        self.receiver_thread.stop()

    def join(self):
        self.receiver_thread.join()

class MQTTReceiverThread(threading.Thread):
    def __init__(self, host, port, topic):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.stop_event = threading.Event()

    def run(self):
        self.client.connect(self.host, self.port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        self.parent.data.append(msg.payload.decode())

    def send_response(self, response):
        self.client.publish(self.topic, response)

    def stop(self):
        self.stop_event.set()
        self.client.disconnect()


def main():
    # Create a Receiver object and start the MQTT thread
    receiver = Receiver(MQTTReceiverThread(host="localhost", port=1883, topic="mytopic"))

    # Do some other work here, such as processing the received data
    while True:
        data = receiver.get_data()
        if data:
            print("Received data:", data)
            receiver.send_response("ACK")

    # Stop and exit the MQTT thread when you are done
    receiver.stop()
    receiver.join()
    
    
    
class CANReceiverThread(threading.Thread):
    def __init__(self, channel, bustype):
        threading.Thread.__init__(self)
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            message = self.bus.recv()
            self.parent.data.append(message)

    def send_response(self, response):
        self.bus.send(response)

    def stop(self):
        self.stop_event.set()

class TCPReceiverThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.conn, self.addr = self.sock.accept()
        self.stop_event = threading.Event()

    def run(self):
        with self.conn:
            print("Connected by", self.addr)
            while not self.stop_event.is_set():
                data = self.conn.recv(1024)
                if not data:
                    break
                self.parent.data.append(data)

    def send_response(self, response):
        self.conn.send(response)

    def stop(self):
        self.stop_event.set()
        self.conn.close()
        
        
class SerialReceiverThread(threading.Thread):
    def __init__(self, port, baudrate):
        threading.Thread.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port, self.baudrate)
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            data = self.serial.readline()
            self.parent.data.append(data)

    def send_response(self, response):
        self.serial.write(response)

    def stop(self):
        self.stop_event.set()
        self.serial.close()

if __name__ == "__main__":
    main()
