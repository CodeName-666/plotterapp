

from receiver_thread import ReceiverThread
from telnetlib import Telnet
from .telnet_config import TelnetConfig



class TelnetServerConnection(ReceiverThread):

    def __init__(self) -> None:
        ReceiverThread.__init__(self)

    
server = telnetlib.Telnet()
server.bind((HOST, PORT))
server.listen(1)
