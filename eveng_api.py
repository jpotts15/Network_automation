#!/usr/bin/env python3
import requests
import json
import telnetlib
import getpass

password = getpass()
login_url = 'http://192.168.2.15/api/auth/login'
cred = '{"username":"admin","password":password}'


s = requests.Session()
r = s.post(login_url, data=cred)
print(r)
#start = s.get('http://192.168.2.15/api/labs/automation.unl/nodes/1/start')
t = s.get('http://192.168.2.15/api/labs/automation.unl/nodes')
raw = t.json()
nodes = raw['data']
print(nodes)
node1= nodes['1']
#for node in nodes.values():
#    print(node['url'])
device1 = {'1':node1['url']}
print(device1['1'])
print(("http://192.168.2.15/api/labs/automation.unl/nodes/1"+device1['1']))
#tn = telnetlib.Telnet("http://192.168.2.15/api/labs/automation.unl/nodes/1", device1['1'])
#tn.write(b"\r\n")
#a = tn.write(b"show ip int bri\n")
#print(a)
