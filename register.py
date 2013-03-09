#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser
import os


def register(ip):
    secret = None
    while not secret:
        body = json.dumps({'username': 'bettseLight', 'devicetype': 'python'})
        url = 'http://%s/api/' % (ip)
        r = requests.post(url, data=body)
        data = json.loads(r.content)[0]
        if(data.has_key('success')):
            secret = data['success']['username']
            print "Key is %s" % secret
        if(data.has_key('error')):
            print "Please push the button on the Phlips Hue Hub"
            sleep(0.5)
    if os.path.isfile('hue.cfg'):
        config = ConfigParser.RawConfigParser()
        config.set('hue', 'secret', secret)
        with open('hue.cfg', 'wb') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('hue.cfg')
    ip = config.get('hue', 'ip')
    register(ip)
