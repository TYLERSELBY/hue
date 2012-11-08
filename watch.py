#!/usr/bin/python
from datetime import datetime
from dhcpmonitor import DHCPMonitor
from light import Light
import ConfigParser

light = None

def basicprint(hwaddr, event, info):
    if(event == 'incoming'):
        print datetime.now(), info['dhcpClientID'], " has arrived"
    elif(event == 'outgoing'):
        print datetime.now(), info['dhcpClientID'], " has departed"

def togglelight(hwaddr, event, info):
    if(event == 'incoming'):
        light.on()
    elif(event == 'outgoing'):
        light.off()

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('hue.cfg')
    ip = config.get('hue', 'ip')
    secret = config.get('hue', 'secret')
    light = Light(ip, secret, 2)

    d = DHCPMonitor(ip='10.0.1.1')
    #iMac
    #d.register('D8:30:62:4C:F6:2A','incoming', basicprint)
    #iPhone
    d.register('04:F7:E4:16:75:A3','incoming', togglelight)
    d.register('04:F7:E4:16:75:A3','outgoing', togglelight)
    #run
    d.run()
