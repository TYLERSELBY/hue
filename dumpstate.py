#!/usr/bin/python
import requests
from time import sleep
import json
import ConfigParser
import pprint
import sqlite3

config = ConfigParser.RawConfigParser()
config.read('hue.cfg')

ip = config.get('hue', 'ip')
secret = config.get('hue', 'secret')
db = config.get('hue', 'db')

conn = sqlite3.connect(db)
c = conn.cursor()

url = 'http://%s/api/%s/' % (ip, secret)
r = requests.get(url)
json = json.loads(r.text)
lights = json['lights']

for key in lights:
    columns = [x for x in lights[key]['state'].keys()]
    columns = ['id'] + columns
    query = "insert into lightstate ('" + '\',\''.join(columns)  + "')  values (" + ','.join(['?' for x in columns]) + ");"
    print query
    values = [str(lights[key]['state'][x]) for x in columns if x != 'id']
    values = [key] + values
    print values
    c.execute(query, values)
    #pprint.pprint(lights[key]['state'])


# Save (commit) the changes
conn.commit()

# We can also close the cursor if we are done with it
c.close()
