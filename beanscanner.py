# Bean iBeacon Scanner
# 2015 Kevin Anthony (kevin@anthonynet.org)
# --------------------
# Simple wireless temperature logger using a Lightblue Bean.
# 
# Scans for broadcasting iBeacons and checks if they are in the beacon list
# and extracts the data to send to ThingSpeak
#

try:
    from config import *
except ImportError:
    print("Could not load configuration from config.py")
    sys.exit(1)

import time
import logging
import logging.handlers
import sys
import signal

# External modules
import blescan
import thingspeak
import bluetooth._bluetooth as bluez

def signal_handler(signal, frame):
    print "Caught signal, shutting down"
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
 
class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level
 
    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("Bean iBeacon Scanner Startup")

try:
    sock = bluez.hci_open_dev(BT_DEV_ID)
except:
    logger.error("error accessing bluetooth device...")
    sys.exit(1)

last_seen = {}

logger.info("Scanning for the following beacons: ")
for my_beacon in MY_BEACONS:
    last_seen[my_beacon[0]] = 0;
    logger.info("  %s", my_beacon[0])

logger.info("Starting scan..")
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    beacon_list = blescan.parse_events(sock, 10)
    for beacon in beacon_list:
        for my_beacon in MY_BEACONS:
            if my_beacon[0] in beacon:
                logger.debug("Received iBeacon %s", my_beacon[0])
                # Throttles messages from the same beacon within 30 seconds of each other to stop
                # situations where the beacon advertising period was picked up more than once
                if time.time() - last_seen[my_beacon[0]] < 30:
                    logger.debug("  Throttling updates for %s still", my_beacon[0])
                else:
                    last_seen[my_beacon[0]] = time.time()
                    beacon_info = beacon.split(',')
                    voltage = ( float(beacon_info[2]) / 100 )
                    temperature = beacon_info[3]
                    logger.debug("  UUID: %s", beacon_info[1])
                    logger.debug("  Volt: %s", voltage)
                    logger.debug("  Temp: %s", temperature)
                    logger.debug("  RSSi: %s", beacon_info[5])
        
                    channel = thingspeak.channel( my_beacon[1], my_beacon[2] );
                    try:
                        response = channel.update([voltage,temperature])
                        data = response.read()
                        if response.status == 200:
                            logger.debug("Sent to ThingSpeak")
                        else:
                            logger.warning("Bad response from ThingSpeak, probably did not work")
                    except:
                        logger.error("Could not communicate with ThingSpeak")

