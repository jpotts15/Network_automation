#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command and mutli devices

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

#Add list to be a list of devices
devices = []

#define devices as a dictionary
cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.2.179",
    "username": username_input,
    "password": password_input,
}
#Append this device to a list of devices
devices.append(cisco1)

#repeat for more devices
cisco2 = {
    "device_type": "cisco_ios",
    "host": "192.168.2.181",
    "username": username_input,
    "password": password_input,
}
devices.append(cisco2)

# Show commands that we will run
command1 = "show ip int brief"
command2 = "show ip route"

#loop over the list of devices with each to initiate connection handler with all the variables from the device variable (dict) then send it commands
for device in devices:
    with ConnectHandler(**device) as net_connect:
        output1 = net_connect.send_command(command1)
        output2 = net_connect.send_command(command2)

# print outputs inside the loop
    print("Output of " + device["host"] + "\n" + output1 + "\n")
    print("Output of " + device["host"] + "\n" + output2 + "\n")
