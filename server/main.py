from config import Game_properties as gp
from game_room import Game_room
import socket as sk
import threading
import time


class Server:
    def __init__(self, server_socket1, server_address1, server_socket2, server_address2):
        self.server_socket1 = server_socket1
        self.server_address1 = server_address1

        self.server_socket2 = server_socket2
        self.server_address2 = server_address2

        self.connected_clients = []
        self.game_rooms = []
        self.waiting = False

        self.server_socket1.bind(self.server_address1)
        self.server_socket2.bind(self.server_address2)
        self.server_socket1.settimeout(0.1)
        self.server_socket2.settimeout(0.1)

        
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            # Wait for a client to send data
            try:
                data, client_address = self.server_socket2.recvfrom(1024)
            except TimeoutError:
                continue
            if client_address in self.connected_clients:
                continue
            
            threading.Thread(target=self.handle_messages).start()
            print(self.connected_clients)
            print(self.game_rooms)

            # Handles creating and joining game rooms
            if self.waiting:
                self.game_rooms[-1][1] = client_address
                threading.Thread(target=self.handle_game, args=(self.game_rooms[-1],)).start()
            else:
                self.game_rooms.append([client_address, None])
            
            self.waiting = not self.waiting

            # Appends the client to the connected clients
            self.connected_clients.append(client_address)

    def handle_game(self, game_room):
        self.game_rooms[-1].append(Game_room(game_room, self.server_socket1))

    def handle_messages(self):
        while self.run:
            print('a')
            try:
                data, client_address = self.server_socket1.recvfrom(1024)
                print(data, client_address)
            except TimeoutError:
                continue
            time1 = time.time()
            if client_address not in self.connected_clients:
                continue
            
            for room in self.game_rooms:
                if client_address in room:
                    index = room.index(client_address)
                    game_room = room
            if len(game_room) != 3:
                print(len(game_room))
                continue
            
            print(game_room, 'gamerooom')
            try:
                if index == 0:
                    game_room[2].client2.receive_info(data)
                else:
                    game_room[2].client1.receive_info(data)
            except IndexError as e:
                print(e)
            print(time.time() - time1)
        

Server(sk.socket(sk.AF_INET, sk.SOCK_DGRAM), ('0.0.0.0', 12345),
       sk.socket(sk.AF_INET, sk.SOCK_DGRAM), ('0.0.0.0', 12346))
