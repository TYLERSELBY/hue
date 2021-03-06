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
        self.extra = {
            'incoming': {},
            'outgoing': {}
        }

    def register(self, hwaddr='*', event='incoming', method='print', extra = {}):
        self.hook[event][hwaddr] = method
        self.extra[event][hwaddr] = extra

    def signal_handler(self, signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

    def listOnline(self, users):
        online = []
        for mac in users:
            if(users[mac].has_key('wirelessTimeAssociated')):
                online.append(mac)
        return online

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

    def perform_action(self, users, group, direction):
        for client in group:
            if(self.hook[direction].has_key(client)):
                self.hook[direction][client](client, direction, users[client], self.extra[direction][client])
            if(self.hook[direction].has_key('*')):
                self.hook[direction]['*'](client, direction, users[client], self.extra[direction]['*'])

    def run(self):
        online = set()
        was_online = set()
        while 1:
            users = self.restructure(self.collect_snmp())
            online = set(self.listOnline(users))
            new = (online - was_online)
            old = (was_online - online)
            self.perform_action(users, new, 'incoming')
            self.perform_action(users, old, 'outgoing')
            was_online = online
            sleep(1)


