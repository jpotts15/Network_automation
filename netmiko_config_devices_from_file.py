#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass
import csv
import re

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command.
#uses a device file input (csv) to then run a set of commands against those from the commands file

#enter file names
device_file = input("Enter device list filename (with csv extension): ")
check = True
prechecks = False
postchecks = False
while check == True:
    print("Do you have prechecks to run: ")
    #check response, make answer lower and strip to y or n
    prechecks_check = str(input('Yes or No: ').lower().strip())
    if prechecks_check[0] == 'y':
        prechecks_commands_file = input("Enter prechecks filename: ")
        prechecks = True
        check = False
    if prechecks_check[0] != 'y':
    	check = False

configure_commands_file = input("Enter configuration commands filename: ")

check = True
while check == True:
    print("Do you have postchecks to run: ")
    #check response, make answer lower and strip to y or n
    postchecks_check = str(input('Yes or No: ').lower().strip())
    if postchecks_check[0] == 'y':
        postchecks_commands_file = input("Enter postchecks filename: ")
        postchecks = True
        check = False
    if postchecks_check[0] != 'y':
    	check = False

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
            if prechecks == True:
                with open(prechecks_commands_file) as precheck_command_file:
                    for line in precheck_command_file:
                        output1 = net_connect.send_command(line)
# print outputs
                        print("\n" + output1 + "\n")
                prechecks = False
            with open(configure_commands_file) as command_file:
                commands = []
                for line in command_file:
                    commands.append(line)
                output1 = net_connect.send_config_set(commands)
# print outputs
                print("\n" + output1 + "\n")
                    #print(re.findall("(([Ff]*|[Gg]()).*[Ee]thernet...)",output1))
                    #print(re.findall(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",output1))
            if postchecks == True:
                with open(postchecks_commands_file) as postcheck_command_file:
                    for line in postcheck_command_file:
                        output1 = net_connect.send_command(line)
    # print outputs
                        print("\n" + output1 + "\n")
                postchecks = False
        #print("\n" + output2 + "\n")
