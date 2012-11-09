#!/usr/bin/python
from time import sleep
import ConfigParser
from light import Light
import sys

config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
light = config.get('hue', 'light')
numlights = int(config.get('hue', 'numlights'))

if(len(sys.argv) > 1):
    light = sys.argv[1]

if(len(sys.argv) > 2):
    x = int(sys.argv[2])
else:
    x = 100

if light.strip() == 'all':
    lights = [Light(ip, secret, x) for x in range(1, numlights+1)]
else:
    lights = [Light(ip, secret, light)]

while x > 0:
    x = x - 1
    for light in lights:
        #print "on", light.number()
        light.on()
        sleep(1)
        #print "off", light.number()
        light.off()
        sleep(1)
