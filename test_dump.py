import socket
import time

# Define the remote server address
remote_server_address = ('localhost', 30003)  # Replace 'remote_host' with the actual hostname or IP address
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


t_start = time.time()

try:
    # Connect to the remote server
    client_socket.connect(remote_server_address)
    print(f"Connected to {remote_server_address[0]}:{remote_server_address[1]}")
    # Set a timeout for receiving data (30 seconds)
    client_socket.settimeout(10)
    while True:
        time.sleep(0.5)
        # Receive and print data from the remote server
        data = client_socket.recv(1024)  # 1024 is the buffer size
        if not data:
            break  # No more data, break the loop
        print(f"Received data: {data.decode('utf-8')}")
        if(time.time()-t_start > 60):
            print("program run for 60 seconds")
            break

except ConnectionRefusedError:
    print("Connection to the remote server was refused.")
except socket.timeout:
    print("Connection timed out.")
except KeyboardInterrupt:
    print("Client stopped by the user.")
finally:
    # Close the client socket
    client_socket.close()