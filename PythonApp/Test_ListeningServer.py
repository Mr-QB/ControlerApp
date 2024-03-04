from DataSocket import *
# Create an instance of DataSocket and start the server

if __name__ == '__main__':
    data_socket = DataSocket('localhost', 12345)  # Use '0.0.0.0' as host to listen on all available network interfaces
    data_socket.start_server()
