import socket as sk
import threading
import pickle
import random


class Server:
    def __init__(self, server_socket, server_address):
        self.server_socket = server_socket
        self.server_address = server_address

        self.connected_clients = []
        self.game_rooms = []
        self.waiting = False

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(2)
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            print(self.connected_clients)
            print(self.game_rooms)
            # Wait for a client to connect
            client_socket, client_address = self.server_socket.accept()

            # Handles creating and joining game rooms
            if self.waiting:
                self.game_rooms[-1][1] = (client_socket, client_address)
                direction = [bool(random.randint(0, 1)), bool(random.randint(0, 1))]
                self.game_rooms[-1][0][0].send(pickle.dumps(direction))
                self.game_rooms[-1][1][0].send(pickle.dumps([not direction[0], direction[1]]))
            else:
                self.game_rooms.append([(client_socket, client_address), None])
            
            self.waiting = not self.waiting

            # Appends the client to the connected clients
            self.connected_clients.append((client_socket, client_address))

            # Starts a thread that will handle the client
            threading.Thread(target=self.handle_client, 
                            args=(client_socket, 
                                client_address)).start()

    def handle_client(self, socket, address):
        print(f"Connection from {address} established.")
        
        try:
            while True:
                response = socket.recv(1024).decode()
                for client_socket, client_address in self.connected_clients:
                    if (client_socket, client_address) != (socket, address):
                        client_socket.send(("enemy:"+response).encode())
                if not response:
                    break  # No more data from the client, exit the loop
                print(response)
        except ConnectionResetError:
            pass  # Handle the case where the client abruptly disconnects
        
        print(f"Connection from {address} closed.")
        self.connected_clients.remove((socket, address))
        socket.close()


Server(sk.socket(sk.AF_INET, sk.SOCK_STREAM), ('0.0.0.0', 12345))
