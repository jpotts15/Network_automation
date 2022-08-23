#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass
import csv
import re

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command.
#uses a device file input (csv) to then run a set of commands against those from the commands file

#enter file names
device_file = input("Enter device list filename (with csv extension): ")
commands_file = input("Enter command filename: ")

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

# Show commands that we will run
#command1 = "show ip int brief"
#command2 = "show ip route"

#define the device as a dictionary
with open(device_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        device = {
        "device_type": row['device_type'],
        "host": row['host'],
        "username": username_input,
        "password": password_input,
        }
#initiate connection handler with all the variables from the device variable (dict) then send it commands
        with ConnectHandler(**device) as net_connect:
            with open(commands_file) as command_file:
                for line in command_file:
                    output1 = net_connect.send_command(line)

# print outputs
                    print("\n" + output1 + "\n")
                    print(re.findall("(([Ff]*|[Gg]()).*[Ee]thernet...)",output1))
                    print(re.findall(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",output1))
        #print("\n" + output2 + "\n")
