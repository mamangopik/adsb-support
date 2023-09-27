import socket
import time
import json
import paho.mqtt.client as mqtt

data_buffer = {
    'raw_data':[]
}

# Define the remote server address
remote_server_address = ('localhost', 30003)  # Replace 'remote_host' with the actual hostname or IP address
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def push_mqtt():
    # Define MQTT broker information
    broker_address = "broker.hivemq.com"  # Replace with your MQTT broker address
    broker_port = 1883  # Default MQTT port
    topic = "test/topic"  # The MQTT topic to publish to
    # Create an MQTT client
    client = mqtt.Client()
    # Connect to the MQTT broker
    client.connect(broker_address, broker_port)
    # Publish a message
    message = "Hello, MQTT!"
    client.publish(topic, message)
    # Disconnect from the broker
    client.disconnect()

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
        # print(f"Received data: {data.decode('utf-8')}")
        data_buffer['raw_data'].append(data.decode('utf-8'))
        if len(data_buffer['raw_data'])>50:
            try:
                push_mqtt(data)
                data_buffer['raw_data']=[] #reset buffer
            except:
                pass

except ConnectionRefusedError:
    print("Connection to the remote server was refused.")
except socket.timeout:
    print("Connection timed out.")
except KeyboardInterrupt:
    print("Client stopped by the user.")
finally:
    # Close the client socket
    client_socket.close()