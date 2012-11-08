#!/usr/bin/python
import requests
from time import sleep
import json

class Light:
    def __init__(self, ip, secret, lightnum):
        self.ip = ip
        self.secret = secret
        self.lightnum = lightnum

    def brightness(self, i):
        if(i == 'full'):
            i = 255
        if(i > 255):
            i = 255
        bri = json.dumps({'bri': i, 'on': True})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=bri)

    def on(self):
        body = json.dumps({'on': True})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)

    def off(self):
        body = json.dumps({'on': False})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)

    def number(self):
        return self.lightnum

    def getstate(self):
        url = 'http://%s/api/%s/lights/%s/' % (self.ip, self.secret, self.lightnum)
        r = requests.get(url)
        return json.loads(r.content)['state']

    def concentrate(self):
        body = json.dumps({u'on': True, u'hue': 13122, u'colormode': u'ct', u'effect': u'none', u'alert': u'none', u'xy': [0.5119, 0.4147], u'reachable': True, u'bri': 219, u'sat': 211, u'ct': 233})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)

    def energize(self):
        body = json.dumps({u'on': True, u'hue': 13122, u'colormode': u'ct', u'effect': u'none', u'alert': u'none', u'xy': [0.5119, 0.4147], u'reachable': True, u'bri': 203, u'sat': 211, u'ct': 156})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)

    def reading(self):
        body = json.dumps({u'on': True, u'hue': 13122, u'colormode': u'ct', u'effect': u'none', u'alert': u'none', u'xy': [0.5119, 0.4147], u'reachable': True, u'bri': 240, u'sat': 211, u'ct': 346})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)

    def relax(self):
        body = json.dumps({u'on': True, u'hue': 13122, u'colormode': u'ct', u'effect': u'none', u'alert': u'none', u'xy': [0.5119, 0.4147], u'reachable': True, u'bri': 144, u'sat': 211, u'ct': 467})
        url = 'http://%s/api/%s/lights/%s/state' % (self.ip, self.secret, self.lightnum)
        r = requests.put(url, data=body)


