#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser
from light import Light


config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
light = config.get('hue', 'light')
numlights = int(config.get('hue', 'numlights'))

duration=600
max_bri=255

if light.strip() == 'all':
    lights = [Light(ip, secret, x) for x in range(1, numlights+1)]
else:
    lights = [Light(ip, secret, light)]

interval = float(duration)/max_bri

#Don't allow internal faster than 2/second
if ( (interval / len(lights)) < .5):
    interval = 0.5

#turn defined lights on but dark
for light in lights:
    light.brightness(1)
    light.on()

for i in range(1, max_bri):
    for light in lights:
        light.brightness(i)
        sleep(interval)
        print "Light %s to level %s" % (light.number(), i)
