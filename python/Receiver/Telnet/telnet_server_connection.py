server = telnetlib.Telnet()
server.bind((HOST, PORT))
server.listen(1)
