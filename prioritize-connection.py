#!/usr/bin/env python3

# import logging
# from logging.handlers import TimedRotatingFileHandler
# from logging import Formatter
import subprocess
import time
from subprocess import call
from subprocess import DEVNULL
# from gpiozero import Buzzer
# import schedule
import sys
# import dotenv

# LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s:%(lineno)d"
# CONNECTIVITY_LOG_FILE = '/home/ravinder/log/connectivity.log'
# connectivity_logger = logging.getLogger('connectivity_logging')
# connectivity_logger.setLevel(logging.DEBUG)
# connectivity_logger_file = TimedRotatingFileHandler(
#     CONNECTIVITY_LOG_FILE, when='D', interval=1, backupCount=3)
# connectivity_logger_file.setLevel(logging.DEBUG)
# connectivity_logger_file.setFormatter(Formatter(LOG_FORMAT))
# connectivity_logger.addHandler(connectivity_logger_file)

# server_config_file = dotenv.find_dotenv('/etc/config/server.conf')
# current_server_config = dotenv.dotenv_values(server_config_file)

def ping():
    pingRc = call(['ping', '-c1', '-w10', '-s0', '8.8.8.8'])
    # pingServer = call(['ping', '-c1', '-w10', '-s0', current_server_config["ADSB_SBS1_HOST"]])
    # return pingRc, pingServer
    return ping,10

def restart_service():
    # modem_logger.info("restart service")
    sys.exit()

#schedule.every(5).minutes.do(restart_service)

def main():

    connectivity = 'eno1'
    failCount = 0
    afterDown = False
    try:
        call(['set-eth0-priority.sh'], stdout=DEVNULL, stderr=DEVNULL)
        # connectivity_logger.info("Connection Interface has been prioritized to "+connectivity)
        pass
    except:
        # connectivity_logger.error("Failed to prioritize Interface to "+connectivity)
        # connectivity_logger
        pass

    time.sleep(3)

    while True:
        rc = ping()
        if(rc[1]):
            print(rc[1])
            # dotenv.set_key(server_config_file, "HAS_CONNECTION",
            #                "False", quote_mode="never")
            # subprocess.run(["systemctl", "restart", "openfortivpn.service"])
        else:
            # dotenv.set_key(server_config_file, "HAS_CONNECTION",
            #     "True", quote_mode="never")
            pass

        # if ping no response success after 10s
        if rc[0]:
            print(rc)
            if failCount < 7:
                failCount += 1
                # connectivity_logger.info('Connection Down')
                time.sleep(3)
                try:
                    # call(['start-modem.sh'], stdout=DEVNULL, stderr=DEVNULL)
                    if connectivity == 'eno1':
                        connectivity = 'wlo1'
                        call(['set-wlan0-priority.sh'], stdout=DEVNULL, stderr=DEVNULL)
                    elif connectivity == 'wlo1':
                        connectivity = 'eno1'
                        call(['set-eth0-priority.sh'], stdout=DEVNULL, stderr=DEVNULL)
                    # connectivity_logger.info("Connection Interface has been prioritized to "+connectivity)
                    time.sleep(5)
                    # continue
                except:
                    # connectivity_logger.error("Failed to prioritize Interface to "+connectivity)
                    pass
            else:
                #schedule.run_pending()
                pass
        # ping succes
        else:
            failCount = 0

            # wait 10s before check connection again
        time.sleep(5)


if __name__ == "__main__":
    # connectivity_logger.info("Starting Script")
    main()