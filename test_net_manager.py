# this code is to test the functionality of net_priority_manager.py
# works on Ubuntu 20.4 LTS machine


import subprocess
import time

# Define the list of network interfaces to test
interfaces = ["eno1", "wlo1"]
# Define the test server to ping
test_server = "8.8.8.8"

ping_result = {}
last_ping_result = {}

# Function to run ping and get metrics
def get_ping_metrics(interface):
    try:
        ping_result = subprocess.check_output(
            ["ping", "-I", interface, "-c", "2", "-q", test_server],
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


last_roll = None
def switch_metric(roll):
    global last_roll
    # print("switch metric","roll",roll,"last_roll",last_roll)
    metric_val = []
    if roll == 0:  #priority eth0
        metric_val = [200,300.400]
    if roll == 1: #priority wlan0
        metric_val = [400,200,300]

    if last_roll != roll:
        try:
            print("network priority changes!")
            subprocess.run(["ifmetric", 'eno1', str(metric_val[0])], check=True)
            time.sleep(1)
            subprocess.run(["ifmetric", 'wlo1', str(metric_val[1])], check=True)
            time.sleep(1)
            last_roll = roll
        except:
            pass


def metric_rule():
    if ping_result['eno1']: #priority eth0
        switch_metric(0)
    else:
        if ping_result['wlo1']: #priority wlan0
            switch_metric(1)
        else:
            print("not connected to internet")

for interface in interfaces:
    ping_result[interface] = False


while 1:
    time.sleep(100)
    for interface in interfaces:
        rtt, packet_loss = get_ping_metrics(interface)
        if rtt is not None and packet_loss is not None:
            ping_result[interface] = True
        if rtt == None or packet_loss == None:
            ping_result[interface] = False

    print(ping_result)

    try:
        metric_rule()
    except Exception as e:
        print("something went wrong",e)