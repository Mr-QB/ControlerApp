import socket
import pickle

class DataSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None

    def start_server(self):
        try:
            # Create a socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind address and port
            self.server_socket.bind((self.host, self.port))

            # Listen for connections
            self.server_socket.listen()
            print(f"Server is listening on {self.host}:{self.port}")

            while True:
                # Accept connection from client
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established.")

                # Receive data from client
                received_data = client_socket.recv(1024)
                if received_data:
                    print(f"Received data from client: {pickle.loads(received_data)}")

                    # Send response back to client (optional)
                    client_socket.send(b"Message received by server!")

                # Close the connection
                client_socket.close()

        except Exception as e:
            print(f"An error occurred while starting the server: {e}")
            # Close the server socket
            if self.server_socket:
                self.server_socket.close()

    def send_data(self, data):
        try:
            # Send pickle data via socket
            self.client_socket.send(pickle.dumps(data))

        except Exception as e:
            print(f"An error occurred while sending data: {e}")

    def close_connection(self):
        try:
            # Close the connection
            self.server_socket.close()
            if self.client_socket:
                self.client_socket.close()
            print("Connection closed.")

        except Exception as e:
            print(f"An error occurred while closing the connection: {e}")