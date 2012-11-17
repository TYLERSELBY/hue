#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser
from light import Light
import sys


config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
light = config.get('hue', 'light')
numlights = int(config.get('hue', 'numlights'))

duration=600
max_bri=254


print "%s <lightnum> <duration> <max_bri>" % sys.argv[0]

if(len(sys.argv) > 1):
    light = sys.argv[1]
if(len(sys.argv) > 2):
    duration = int(sys.argv[2])
if(len(sys.argv) > 3):
    max_bri = sys.argv[3]

if(max_bri == 'full' or int(max_bri) > 254):
    max_bri = 254
else:
    max_bri = int(max_bri)

if light.strip() == 'all':
    lights = [Light(ip, secret, i) for i in range(1, numlights+1)]
else:
    lights = [Light(ip, secret, light)]

#turn defined lights on but dark
for light in lights:
    light.brightness(1)
    light.on()

for light in lights:
    light.setstate({'transitiontime' : duration, 'bri' : max_bri})
