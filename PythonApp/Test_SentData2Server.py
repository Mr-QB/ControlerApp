import socket
import json

def send_data(host, port, data):
    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Setup timeout
        client_socket.settimeout(15)

        # Connect to the server
        client_socket.connect((host, port))

        # Send data
        data_str = json.dumps(data)
        client_socket.sendall(data_str.encode())

        # Receive response (if any)
        try:
            response = client_socket.recv(1024)
            print(f"Received response from server: {response.decode()}")
        except socket.timeout:
            print("Timeout occurred while receiving response from server.")

        # Close the connection
        client_socket.close()

    except Exception as e:
        print(f"An error occurred while sending data: {e}")

if __name__ == '__main__':
    # Test sending data to the server
    data_to_send = {"message": "Hello from client!"}
    send_data('192.168.1.6', 12345, data_to_send)