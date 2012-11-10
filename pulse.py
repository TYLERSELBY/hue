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

print "%s <lightnum> <pulse count> <color>" % sys.argv[0]

if(len(sys.argv) > 1):
    light = sys.argv[1]

if(len(sys.argv) > 2):
    x = int(sys.argv[2])
else:
    x = 100

if(len(sys.argv) > 3):
    color = sys.argv[3]
else:
    color = None

if light.strip() == 'all':
    lights = [Light(ip, secret, x, True) for x in range(1, numlights+1)]
else:
    lights = [Light(ip, secret, light, True)]

state = {}

while x > 0:
    x = x - 1
    #Set to alternate state
    for light in lights:
        state[light.number()] = light.getstate()
        #flash color
        if(color):
            getattr(light, color)()
            pass
        #flash on/off
        else:
            if(state[light.number()]['on']):
                light.off()
            else:
                light.on()
        sleep(1)

    #Set to original state
    for light in lights:
        light.setstate(state[light.number()])
        sleep(1)



