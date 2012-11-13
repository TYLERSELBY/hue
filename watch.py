#!/usr/bin/python
from datetime import datetime
from dhcpmonitor import DHCPMonitor
from light import Light
import ConfigParser

def basicprint(hwaddr, event, info, extra):
    name = hwaddr
    if (info.has_key('dhcpClientID') and info['dhcpClientID'] != ''):
        name = info['dhcpClientID']
    if (event == 'incoming'):
        print "[%s] %s has %s" % (datetime.now(), name, 'arrived')
    elif (event == 'outgoing'):
        print "[%s] %s has %s" % (datetime.now(), name, 'departed')

def togglelight(hwaddr, event, info, lights):
    if(event == 'incoming'):
        #Only turn on between 6:30 and 10:59
        if( (datetime.now().hour > 6 and datetime.now().minute > 30) and (datetime.now().hour < 22 and datetime.now().minute < 59)):
            for light in lights:
                light.on()
    elif(event == 'outgoing'):
        for light in lights:
            light.off()

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('hue.cfg')
    ip = config.get('hue', 'ip')
    secret = config.get('hue', 'secret')
    numlights = int(config.get('hue', 'numlights'))
    lights = [Light(ip, secret, x) for x in range(1, numlights+1)]

    d = DHCPMonitor(ip='10.0.1.1')
    d.register('*','incoming', basicprint)
    d.register('*','outgoing', basicprint)
    #iPhone
    d.register('04:F7:E4:16:75:A3','incoming', togglelight, lights)
    d.register('04:F7:E4:16:75:A3','outgoing', togglelight, lights)
    #run
    d.run()
