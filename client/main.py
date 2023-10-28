import threading
import json
import socket
import time


class Client:
    def __init__(self):
        self.server_password = 'greensock'

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_addr = ('localhost', 12345)
        self.connection_socket.connect(self.connection_addr)

        self.info_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.info_socket.bind(('localhost', 0))
        self.info_addr = ('localhost', 12346)

        self.connection_socket.send(json.dumps((self.info_socket.getsockname(), self.server_password)).encode('utf-8'))

        self.run = True

        threading.Thread(target=self.pulse).start()


    def pulse(self):
        while self.run:
            try:
                self.connection_socket.send(json.dumps('pulse').encode('utf-8'))
                time.sleep(5)
            except Exception as e:
                print(e)
                self.run = False

    
    def main(self):
        while self.run:
            command = input()
            if command == 'dc':
                self.connection_socket.close()
            else:
                self.info_socket.sendto(json.dumps(command).encode('utf-8'), self.info_addr)



c = Client()
c.main()