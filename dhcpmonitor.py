#!/usr/bin/python

from subprocess import Popen, PIPE, STDOUT
from time import sleep
from datetime import datetime
import signal, sys

class DHCPMonitor:
    def __init__(self, ip=None):
        signal.signal(signal.SIGINT, self.signal_handler)
        if(ip):
            self.ip = ip
        self.max_lease_time = 7*24*60*60
        self.hook = {
            'incoming': {},
            'outgoing': {}
        }

    def register(self, hwaddr, event, method):
        self.hook[event][hwaddr] = method

    def signal_handler(self, signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

    def GetInHMS(self, seconds):
        hours = seconds / 3600
        seconds -= 3600*hours
        minutes = seconds / 60
        seconds -= 60*minutes
        if hours == 0:
            return "%02d:%02d" % (minutes, seconds)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def collect_snmp(self):
        command = ['/usr/bin/snmpwalk', '-m', '/usr/share/snmp/mibs/AIRPORT-BASESTATION-3-MIB.txt', '-Os', '-v', '2c', '-c', 'airport', self.ip, 'SNMPv2-SMI::enterprises.apple.airport']
        raw_output = Popen(command, stdout=PIPE).communicate()[0]
        output_dict = {}

        #Handle parsing the raw data and cleaning it up a bit
        for line in raw_output.split('\n'):
            if(line == ""): continue
            k,v = line.strip().split('=')
            if(v.count('INTEGER') > 0):
                v = v.replace('INTEGER:', '')
                v = v.replace('sta(', '')
                v = v.replace(')', '')
                v = int(v)
            elif (v.count('STRING') > 0):
                v = v.replace('STRING:', '')
                v = v.replace('"', '')
                v = v.strip()
            elif (v.count('IpAddress') > 0):
                v = v.replace('IpAddress: ', '')
            else:
                v = v.strip()
                v = v.replace('"', '')
            output_dict[k.strip()] = v
        return output_dict

    def restructure(self, output_dict):
        #Restructure into a dictionary with various attributes for each client
        users = {}
        for key in output_dict:
            if(key.count('.') > 0):
                cat, mac = key.split('.')
                mac = mac.replace('"', '')
                cat = cat.strip()
                mac = mac.strip()
                #0 is the general non-client specific settings
                if(mac == "0"): continue
                if(not users.has_key(mac)):
                    users[mac] = {}
                users[mac][cat] = output_dict[key]
        return users

    def listOnline(self, users):
        online = []
        for mac in users:
            if(users[mac].has_key('wirelessTimeAssociated')):
                online.append(mac)
        return online

    def printOnline(self, users):
        for mac in users:
            if(users[mac].has_key('dhcpClientID')):
                if(users[mac]['dhcpClientID'] == ""):
                    print mac, ": ",
                else:
                    print users[mac]['dhcpClientID'], ": ",
                if(users[mac].has_key('wirelessTimeAssociated')):
                    print self.GetInHMS(users[mac]['wirelessTimeAssociated']), "remaining"
                else:
                    print "Not associated"

    def run(self):
        online = set()
        was_online = set()
        while 1:
            users = self.restructure(self.collect_snmp())
            online = set(self.listOnline(users))
            new = (online - was_online)
            old = (was_online - online)
            if (new):
                for client in new:
                    if(self.hook['incoming'].has_key(client)):
                        self.hook['incoming'][client](client, 'incoming', users[client])
                    if(self.hook['incoming'].has_key('*')):
                        self.hook['incoming']['*'](client, 'incoming', users[client])
            if (old):
                for client in old:
                    if(self.hook['outgoing'].has_key(client)):
                        self.hook['outgoing'][client](client, 'outgoing', users[client])
                    if(self.hook['outgoing'].has_key('*')):
                        self.hook['outgoing']['*'](client, 'outgoing', users[client])


            was_online = online
            sleep(1)


