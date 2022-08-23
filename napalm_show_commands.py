#!/usr/bin/env python3
from napalm import get_network_driver
from netmiko import ConnectHandler
from getpass import getpass
import json
import re

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command.
#uses a device file input (csv) to then run a set of commands against those from the commands file

#enter file names
device_file = input("Enter device list filename (with json extension): ")

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

# Show commands that we will run
#command1 = "show ip int brief"
#command2 = "show ip route"

#define the device as a dictionary
with open(device_file) as json_file:
    reader = json.load(json_file)
    for entry in reader['devices']:
        print(entry)
        device = {
        "device_type": entry['device_type'],
        "host": entry['host'],
        "username": username_input,
        "password": password_input,
        }
#initiate connection handler with all the variables from the device variable (dict) then send it commands
        driver = get_network_driver('ios')
        iosvl2 = driver(entry['host'], username_input, password_input)
        iosvl2.open()

        ios_output = iosvl2.get_facts()
        print (json.dumps(ios_output, indent=4))

        #ios_output = iosvl2.ping('google.com')
        #print (json.dumps(ios_output, sort_keys=True, indent=4))

        iosvl2.close()
