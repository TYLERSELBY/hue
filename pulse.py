#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
light = config.get('hue', 'light')
numlights = int(config.get('hue', 'numlights'))

on = json.dumps({'on': True})
off = json.dumps({'on': False})
lights = [x for x in range(1,numlights+1)]

if light.strip() != 'all':
    lights = [light]

while 1:
    for light in lights:
        url = 'http://%s/api/%s/lights/%s/state' % (ip, secret, light)
        r = requests.put(url, data=on)
        sleep(1)
        r = requests.put(url, data=off)
        sleep(1)
