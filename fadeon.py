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

duration=600
max_bri=255
lights = [x for x in range(1,numlights+1)]

if light.strip() != 'all':
    lights = [light]

interval = float(duration)/max_bri

#Don't allow internal faster than 2/second
if ( (interval / len(lights)) < .5):
    interval = 0.5

#turn defined lights on but dark
on = json.dumps({'on': True, 'bri': 0})
for light in lights:
    url = 'http://%s/api/%s/lights/%s/state' % (ip, secret, light)
    r = requests.put(url, data=on)

for i in range(0,max_bri):
    level = json.dumps({'bri': i})
    for light in lights:
        url = 'http://%s/api/%s/lights/%s/state' % (ip, secret, light)
        r = requests.put(url, data=level)
        if(r.status_code != 200):
            print r.status_code
        sleep(interval)
        print "Light %s to level %s" % (light, level)
