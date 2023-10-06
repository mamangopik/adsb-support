import subprocess
import time

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
        # Handle errors, e.g., if ping fa3.ils
        return None, None


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
            ret_val.append({iface:int(metric)})
        return ret_val
    except subprocess.CalledProcessError as e:
        print(f"Error executing 'route -n': {e}")
        return {'interface':null,'metric':99999}

# Define a custom key function to extract the value for sorting
def custom_key(route):
    if 'eno1' in route:
        return route['eno1']
    elif 'wlo1' in route:
        return route['wlo1']
    else:
        return 0  # Default value in case neither 'eno1' nor 'wlo1' key is present



def find_lower_and_best():
    # Initialize variables to track the best interface
    best_iface = None
    best_iface_metric = None
    best_rtt = float("inf")
    best_packet_loss = 100.0

    routes = get_metric()
    sorted_routes = sorted(routes, key=custom_key)

    # Loop through the interfaces and find the best one
    for interface in interfaces:
        rtt, packet_loss = get_ping_metrics(interface)
        if rtt is not None and packet_loss is not None:
            if rtt < best_rtt or (rtt == best_rtt and packet_loss < best_packet_loss):
                best_iface = interface
                best_rtt = rtt
                best_packet_loss = packet_loss
    
    try:
        lower_old = sorted_routes[0]
        lower_old_iface = list(lower_old.keys())[0]
        lower_old_iface_metric = lower_old[lower_old_iface]

        for route in sorted_routes:
            try:
                metric = route[best_iface]
                best_iface_metric = metric
                break
            except:
                pass

    except:
        pass
    
    if (lower_old_iface is not None) and (lower_old_iface_metric is not None) and (best_iface is not None) and (best_iface_metric is not None) and best_iface:
        # print("unsorted routes",metric)
        # print("sorted routes",sorted_routes)

        print("lower iface",lower_old_iface,end=' ')
        print("with metric",lower_old_iface_metric)
        print("best iface",best_iface,end=' ')
        print("best metric",best_iface_metric)
        print(f"RTT: {best_rtt} ms")
        print(f"Packet Loss: {best_packet_loss}%")

        try:
            subprocess.run(["ifmetric", best_iface, str(lower_old_iface_metric)], check=True)
            time.sleep(5)
            subprocess.run(["ifmetric", lower_old_iface, str(best_iface_metric)], check=True)
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            print(f"Error setting metric for {interface_name}: {e}")
    else:
        print("something went wrong")

find_lower_and_best()