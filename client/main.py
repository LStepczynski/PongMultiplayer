from config import Game_properties as gp
from game import Game
import threading
import json
import socket
import time


class Client:
    def __init__(self):
        self.server_password = 'greensock'

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_addr = ('192.168.0.89', 12345)

        self.info_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.info_socket.bind((input("Input your IP address: "), 0))
        self.info_socket.bind(("192.168.0.89", 0))
        self.info_addr = ('192.168.0.89', 12346)

        self.run = True

        Game(self)

    def connect(self):
        self.connection_socket.connect(self.connection_addr)
        self.connection_socket.send(json.dumps((self.info_socket.getsockname(), self.server_password)).encode('utf-8'))
        threading.Thread(target=self.pulse).start()


    def pulse(self):
        while self.run:
            try:
                self.connection_socket.send(json.dumps('pulse').encode('utf-8'))
                time.sleep(5)
            except Exception as e:
                print(e)
                self.run = False

    
    def receive_commands(self):
        while self.run:
            try:
                data, addr = self.info_socket.recvfrom(1024)
                data = json.loads(data.decode('utf-8'))
                print(data)
            except Exception as e:
                print(e)


    def main(self):
        while self.run:
            command = input()
            if command == 'dc':
                self.connection_socket.close()
            else:
                self.info_socket.sendto(json.dumps(command).encode('utf-8'), self.info_addr)



c = Client()
c.main()