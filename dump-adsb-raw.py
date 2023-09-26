import socket
import time

# Define the server address
server_address = ('localhost', 30003)
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the server address
server_socket.bind(server_address)
# Listen for incoming connections
server_socket.listen(1)  # 1 is the maximum number of queued connections
print(f"Server is listening on {server_address[0]}:{server_address[1]}")
# Set the maximum duration for the server to run (30 seconds)
max_duration = 30  # in seconds
start_time = time.time()
try:
    while (time.time() - start_time) < max_duration:
        # Wait for a connection
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        # Receive and print data from the client
        data = client_socket.recv(1024)  # 1024 is the buffer size
        if not data:
            break  # No more data, break the loop
        print(f"Received data: {data.decode('utf-8')}")
except KeyboardInterrupt:
    print("Server stopped by the user.")
finally:
    # Clean up the server socket
    server_socket.close()
