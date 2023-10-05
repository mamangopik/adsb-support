import subprocess

# Define the list of network interfaces to test
interfaces = ["eno1", "wlo1"]

# Define the test server to ping
test_server = "8.8.8.8"

# Function to run ping and get metrics
def get_ping_metrics(interface):
    try:
        ping_result = subprocess.check_output(
            ["ping", "-I", interface, "-c", "4", "-q", test_server],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        # Extract RTT and packet loss from the ping result
        rtt_line = [line for line in ping_result.split("\n") if "rtt min/avg/max/mdev" in line][0]
        packet_loss_line = [line for line in ping_result.split("\n") if "packet loss" in line][0]

        rtt = float(rtt_line.split("/")[4])
        packet_loss = float(packet_loss_line.split(",")[2].split("%")[0])

        return rtt, packet_loss
    except subprocess.CalledProcessError as e:
        # Handle errors, e.g., if ping fails
        return None, None

# Initialize variables to track the best interface
best_interface = None
best_rtt = float("inf")
best_packet_loss = 100.0

# Loop through the interfaces and find the best one
for interface in interfaces:
    rtt, packet_loss = get_ping_metrics(interface)
    if rtt is not None and packet_loss is not None:
        if rtt < best_rtt or (rtt == best_rtt and packet_loss < best_packet_loss):
            best_interface = interface
            best_rtt = rtt
            best_packet_loss = packet_loss

# Print the best interface and metrics
if best_interface:
    print(f"Best Interface: {best_interface}")
    print(f"RTT: {best_rtt} ms")
    print(f"Packet Loss: {best_packet_loss}%")
else:
    print("No valid interface found or all interfaces failed.")




# You can add logic here to set the best interface as the default route if desired.

def get_metric():
    try:
        route_output = subprocess.check_output(["route"], universal_newlines=True)
        # print(type(route_output),route_output)
        rows = route_output.split('\n')[2:-1]
        ret_val = []
        for row in rows:
            cols = row.replace(' ','#')
            colstring = ' '
            prev_char = ''
            for char in cols:
                if colstring[-1] == '#' and char == '#':
                    pass
                else:
                    colstring+= char
            colstring = colstring.replace(' ','')
            cols = colstring.split('#')

            iface = cols[7]
            metric = cols[4]
            ret_val.append({iface:metric})
        return ret_val
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'route -n': {e}")
        return {'interface':null,'metric':99999}

metric = get_metric()
print(metric)