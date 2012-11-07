#!/usr/bin/python
from time import sleep
import ConfigParser
from light import Light

config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
light = config.get('hue', 'light')
numlights = int(config.get('hue', 'numlights'))

if light.strip() == 'all':
    lights = [Light(ip, secret, x) for x in range(1, numlights+1)]
else:
    lights = [Light(ip, secret, light)]

while 1:
    for light in lights:
        #print "on", light.number()
        light.on()
        sleep(1)
        #print "off", light.number()
        light.off()
        sleep(1)
