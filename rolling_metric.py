import subprocess
import time

# Define the test server to ping
test_server = "8.8.8.8"

# Function to run ping and get metrics
def get_ping_metrics():
    try:
        ping_result = subprocess.check_output(
            ["ping", "-c", "4", "-q", test_server],
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


def switch_metric(roll):
    print("switch metric")
    metric_val = []
    if roll == 0:
        metric_val = [200,300.400]
    if roll == 1:
        metric_val = [400,200,300]
    if roll == 2:
        metric_val = [300,400,200]
    try:
        subprocess.run(["ifmetric", 'eno1', str(metric_val[0])], check=True)
        time.sleep(1)
        subprocess.run(["ifmetric", 'wlo1', str(metric_val[1])], check=True)
        time.sleep(1)
        subprocess.run(["ifmetric", 'wwan0', str(metric_val[2])], check=True)
        time.sleep(1)
    except:
        pass


fail  = 0
roll = 0
while 1:
    rtt, packet_loss = get_ping_metrics()
    print("ping duration:",rtt,"packet lost:",packet_loss)
    if rtt == None or packet_loss == None:
        fail +=1
    if fail >= 7:
        fail = 0
        switch_metric(roll)
        roll+=1
        if roll == 3:
            roll = 0
    
    time.sleep(5)