#!/usr/bin/env python3

import subprocess
import time
from subprocess import call
from subprocess import DEVNULL

import sys


def ping():
    pingRc = call(['ping', '-c1', '-w10', '-s0', '8.8.8.8'])
    return ping,999

def restart_service():
    # modem_logger.info("restart service")
    sys.exit()

#schedule.every(5).minutes.do(restart_service)

def main():

    connectivity = 'eno1'
    failCount = 0
    afterDown = False
    try:
        print('1')
        subprocess.run(["ifmetric", 'eno1', str(200)], check=True)
        subprocess.run(["ifmetric", 'wlo1', str(300)], check=True)
        # call(['set-eth0-priority.sh'], stdout=DEVNULL, stderr=DEVNULL)
        # connectivity_logger.info("Connection Interface has been prioritized to "+connectivity)
        pass
    except:
        print('2')
        # connectivity_logger.error("Failed to prioritize Interface to "+connectivity)
        # connectivity_logger
        pass

    time.sleep(3)

    while True:
        print('3')
        rc = ping()
        if(rc[1]):
            print('4')
            print(rc[1])
        else:
            print('5')
            pass

        # if ping no response success after 10s
        if rc[0]:
            print('6')
            print(rc)
            print("fail cnt=",failCount)
            if failCount < 3:
                print('7')
                failCount += 1
                # connectivity_logger.info('Connection Down')
                time.sleep(3)
                try:
                    print('8')
                    # call(['start-modem.sh'], stdout=DEVNULL, stderr=DEVNULL)
                    if connectivity == 'eno1':
                        print('9')
                        connectivity = 'wlo1'
                        subprocess.run(["ifmetric", 'eno1', str(300)], check=True)
                        subprocess.run(["ifmetric", 'wlo1', str(200)], check=True)
                        # call(['set-wlan0-priority.sh'], stdout=DEVNULL, stderr=DEVNULL)
                    elif connectivity == 'wlo1':
                        print('10')
                        connectivity = 'eno1'
                        subprocess.run(["ifmetric", 'eno1', str(200)], check=True)
                        subprocess.run(["ifmetric", 'wlo1', str(300)], check=True)
                    time.sleep(5)
                    # continue
                except:
                    print('11')
                    # connectivity_logger.error("Failed to prioritize Interface to "+connectivity)
                    pass
            else:
                print('12')
                #schedule.run_pending()
                pass
        # ping succes
        else:
            print('13')
            failCount = 0

            # wait 10s before check connection again
        time.sleep(5)


if __name__ == "__main__":
    # connectivity_logger.info("Starting Script")
    main()