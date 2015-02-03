Bean iBeacon Scanner
====================

Simple wireless temperature logger using a Lightblue Bean.

Use the included arduino sketch to program the bean to generate a temporary iBeacon updated with the voltage and temperature each time.

The beanscanner.py will listen on a BTLE interface for iBeacon messages from defined UUIDs and parse and send them to ThingSpeak. This is intended to run on a RaspberryPi with a BTLE adapter.

Requires the following python modules:

blescan - https://github.com/switchdoclabs/iBeacon-Scanner-
thingspeak - https://github.com/bergey/thingspeak
bluetooth - python-bluez package on Raspbian

Copy the config.example.py to config.py and edit as needed.
