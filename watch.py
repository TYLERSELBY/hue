#!/usr/bin/python
from datetime import datetime
from dhcpmonitor import DHCPMonitor
from light import Light
import ConfigParser

light = None

def basicprint(hwaddr, event, info):
    name = hwaddr
    if (info.has_key('dhcpClientID') and info['dhcpClientID'] != ''):
        name = info['dhcpClientID']
    if (event == 'incoming'):
        print "[%s] %s has %s" % (datetime.now(), name, 'arrived')
    elif (event == 'outgoing'):
        print "[%s] %s has %s" % (datetime.now(), name, 'departed')

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
    d.register('*','incoming', basicprint)
    d.register('*','outgoing', basicprint)
    #iPhone
    d.register('04:F7:E4:16:75:A3','incoming', togglelight)
    d.register('04:F7:E4:16:75:A3','outgoing', togglelight)
    #run
    d.run()
