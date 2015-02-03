import logging

# hciX Bluetooth Device, get from 'hcitool dev'
BT_DEV_ID = 0

# Beacons you want to scan for, format is "beaconname", "thingspeakchannelapicode", "thingspeakchannel"
MY_BEACONS = [ 
                [ "a100", "AAAAAAAAAAAAAAAA", 12345 ], 
                [ "a101", "BBBBBBBBBBBBBBBB", 12346 ], 
                [ "a102", "CCCCCCCCCCCCCCCC", 12347 ], 
                [ "a103", "DDDDDDDDDDDDDDDD", 12348 ] 
             ]

LOG_FILENAME = "/tmp/beanscanner.log"
# Set to DEBUG for details of every received beacon
LOG_LEVEL    = logging.DEBUG
