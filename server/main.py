from config import Game_properties as gp
from game_room import Game_room
import socket as sk
import threading
import time


class Server:
    def __init__(self, server_input_socket: sk.socket, server_input_address, 
                 server_init_socket: sk.socket, server_init_address):
        
        # Socket used for the game
        self.server_input_socket = server_input_socket 
        self.server_input_address = server_input_address

        # Socket used to init a connection
        self.server_init_socket = server_init_socket
        self.server_init_address = server_init_address

        self.connected_clients = []
        self.game_rooms = []
        self.waiting = False # Variable storing if someone is waiting for a game

        self.server_input_socket.bind(self.server_input_address)
        self.server_init_socket.bind(self.server_init_address)
        
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            # Wait for a client to connect
            self.server_init_socket.listen()

            connection, client_address = self.server_init_socket.accept()
            connection.settimeout(15)

            # Create a threading event
            e = threading.Event()

            # Start lisening for input
            t1 = threading.Thread(target=self.handle_messages, args=(e,))
            t1.start()

            # Start tesing the connection
            t2 = threading.Thread(target=self.handle_connection, args=(connection, e, client_address,))
            t2.start()
            print('a')


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
        self.game_rooms[-1].append(Game_room(game_room, self.server_input_socket))


    def handle_connection(self, connection: sk.socket, event: threading.Event, address):
        while self.run:
            print(self.connected_clients)
            print(self.game_rooms, "--- game")
            try:
                print(connection.recv(1024), "<---------")
            except Exception as e:
                print(e, "ODLLLLLLLLLLLLLLOMCASWDWADAWDWA")
                connection.close()
                event.set()
                self.waiting = not self.waiting
                self.connected_clients.remove(address)
                for room in self.game_rooms:
                    if address in room:
                        self.game_rooms.remove(room)
                return


    def handle_messages(self, event: threading.Event):
        while self.run and not event.is_set():
            try:
                data, client_address = self.server_input_socket.recvfrom(1024)
            except Exception as e: print(e, 'chuuuuuuuuuj')

            # Checks if the device connected to the server
            if client_address not in self.connected_clients:
                continue
            
            # Gets the position of the sender in the self.game_rooms
            for room in self.game_rooms:
                if client_address in room:
                    index = room.index(client_address)
                    game_room = room

            # Accept input only if the game started
            if len(game_room) != 3:
                continue
            
            # Sends data to a correct client
            if index == 0:
                game_room[2].client1.receive_info(data)

            else:
                game_room[2].client2.receive_info(data)
        

Server(sk.socket(sk.AF_INET, sk.SOCK_DGRAM), ('0.0.0.0', 12345),
       sk.socket(sk.AF_INET, sk.SOCK_STREAM), ('0.0.0.0', 12346))
