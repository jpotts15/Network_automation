#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command.

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

#define the device as a dictionary
cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.2.179",
    "username": username_input,
    "password": password_input,
}

# Show commands that we will run
command1 = "show ip int brief"
command2 = "show ip route"

#initiate connection handler with all the variables from the device variable (dict) then send it commands
with ConnectHandler(**cisco1) as net_connect:
    output1 = net_connect.send_command(command1)
    output2 = net_connect.send_command(command2)

# print outputs
print("\n" + output1 + "\n")
print("\n" + output2 + "\n")
