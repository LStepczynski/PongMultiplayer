import threading
import socket as sk


class Server:
    def __init__(self, server_socket, server_address):
        self.server_socket = server_socket
        self.server_address = server_address

        self.connected_clients = []

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(2)
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            # Wait for a client to connect
            client_socket, client_address = self.server_socket.accept()
            self.connected_clients.append((client_socket, client_address))
            threading.Thread(target=self.handle_client, 
                             args=(client_socket, 
                                   client_address, 
                                   len(self.connected_clients)-1)).start()

    def handle_client(self, socket, address, index):
        print(f"Connection from {address} established.")
        socket.send('Welcome'.encode())
        
        try:
            while True:
                response = socket.recv(1024)
                for client_socket, client_address in self.connected_clients:
                    if (client_socket, client_address) != (socket, address):
                        client_socket.send(response)
                if not response:
                    break  # No more data from the client, exit the loop
                print(response.decode())
        except ConnectionResetError:
            pass  # Handle the case where the client abruptly disconnects
        
        print(f"Connection from {address} closed.")
        self.connected_clients.remove((socket, address))
        socket.close()


Server(sk.socket(sk.AF_INET, sk.SOCK_STREAM), ('0.0.0.0', 12345))
