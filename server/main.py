import threading
import socket as sk


class Server:
    def __init__(self, server_socket, server_address):
        self.server_socket = server_socket
        self.server_address = server_address

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(2)
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            # Wait for a client to connect
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address,)).start()

    def handle_client(self, socket, address):
        print(f"Connection from {address} established.")
        socket.send('Welcome'.encode())
        
        try:
            while True:
                response = socket.recv(1024)
                if not response:
                    break  # No more data from the client, exit the loop
                print(response.decode())
        except ConnectionResetError:
            pass  # Handle the case where the client abruptly disconnects
        
        print(f"Connection from {address} closed.")
        socket.close()


Server(sk.socket(sk.AF_INET, sk.SOCK_STREAM), ('0.0.0.0', 12345))
