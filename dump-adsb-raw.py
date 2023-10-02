import socket
import time
import json
import paho.mqtt.client as mqtt
import datetime
import extract_distance

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with error code {rc}")

data_buffer = {
    'distance':[],
    'other_info':[]
}



# Coordinates for comparison
target_coordinates = (-6.27831, 106.82939)
extarctor  = extract_distance.adsb_to_distance(target_coordinates)

# Define the remote server address
remote_server_address = ('localhost', 30003)  # Replace 'remote_host' with the actual hostname or IP address
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def unix_timestamp_to_datetime(unix_timestamp):
    try:
        # Convert the Unix timestamp to a datetime object
        return datetime.datetime.fromtimestamp(unix_timestamp)
    except Exception as e:
        print(f"Error converting Unix timestamp: {e}")
        return None

def push_mqtt(message):
    broker_address = "broker.hivemq.com"
    broker_port = 1883
    topic = "/adsb/nutech/log/message_dump"  
    client = mqtt.Client('adsb'+str(time.time()))
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    time.sleep(5)
    client.publish(topic, message)
    client.disconnect()

# Connect to the remote server
client_socket.connect(remote_server_address)
print(f"Connected to {remote_server_address[0]}:{remote_server_address[1]}")

start_time = time.time()
while True:
    print(len(data_buffer['distance']))
    data = client_socket.recv(1024)
    try:
        lines = str(data.decode('utf-8'))
        lines = lines.split('\n')
        for line in lines:
            distance = extarctor.get_distance(str(line.strip()))
            if distance:
                data_buffer['distance'].append(distance)
    except:
        pass

    elapsed_time = time.time()-start_time
    if elapsed_time > 15:
        try:
            converted_datetime = str(unix_timestamp_to_datetime(time.time()))
            payload = {
                'distance_message_km':data_buffer['distance'],
                'timestamp':converted_datetime
            }
            mqtt_msg = str(json.dumps(payload))
            push_mqtt(mqtt_msg)
            print('message sent to mqtt broker')
        except Exception as e:
            print(e)
        data_buffer['distance']=[] #reset buffer
        start_time = time.time()

client_socket.close()