#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser
import sys

config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
numlights = int(config.get('hue', 'numlights'))

def usage():
    print "./setlight.py (all|light#) (full|[0-255])"
    sys.exit(0)

if(len(sys.argv) < 2):
    usage()

light = sys.argv[1]
bri = sys.argv[2]
if(bri == 'full'): bri = 255

bri = json.dumps({'bri': bri, 'on': True})
lights = [x for x in range(1,numlights+1)]

if light.strip() != 'all':
    lights = [light]

for light in lights:
    url = 'http://%s/api/%s/lights/%s/state' % (ip, secret, light)
    r = requests.put(url, data=bri)
