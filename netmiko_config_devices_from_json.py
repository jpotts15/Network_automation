#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass
import json
import re

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md example Executing show command.
#uses a device file input (csv) to then run a set of config commands against those from the commands file
#This script is for running configs against devices as netmiko has different commands
#based on the priv level of the prompt

#enter file names
device_file = input("Enter device list filename (with json extension): ")
check = True
prechecks = False
device_config_commands = False
postchecks = False
#Prompt for file of commands to run before making changes
#Generic while loop used elsewhere so will explain here but not down the line
while check == True:
    print("Do you have prechecks to run: ")
    #check response, make answer lower and strip to y or n
    prechecks_check = str(input('Yes or No: ').lower().strip())
    #If yes ask for filename and store as variable
    if prechecks_check[0] == 'y':
        prechecks_commands_file = input("Enter prechecks filename: ")
        prechecks = True
        check = False
    #If checks is not yes then exit loop
    if prechecks_check[0] != 'y':
    	check = False

#ask for config command file
#Another loop for configss
check = True
while check == True:
    print("Do you have configuration changes to run: ")
    configure_commands_file_check = str(input('Yes or No: ').lower().strip())
    if configure_commands_file_check[0] == 'y':
        configure_commands_file = input("Enter configure commands filename: ")
        device_config_commands = True
        check = False
    if configure_commands_file_check[0] != 'y':
    	check = False

#Another loop for post checks
check = True
while check == True:
    print("Do you have postchecks to run: ")
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

##config parser to replace variables in configs from json file
#open file with device configs (json)
with open(device_file) as json_file_parser:
    #open the object in json
    reader = json.load(json_file_parser)
    #loop through devices in json file
    for json_device_entries in reader['devices']:
        #set a new dict variable to the nested vars dict
        device_vars = json_device_entries['vars']
        #open file with commands
        with open(configure_commands_file) as command_file:
            #create new per device config files
            with open(json_device_entries["hostname"]+"_parsed_"+configure_commands_file, "w") as parsed_command_file:
                #loop through the lines in the commands file
                for parser_line in command_file:
                    #create new variable and set it to the parser line
                    parsed_line = parser_line
                    #loop through the dict keys in the vars dict
                    for key in device_vars:
                        #check if key matches something in the line from the commands file
                        if key in parsed_line:
                            #if it matches repalce it with the key value from the vars dict
                            parsed_line = parsed_line.replace(key, device_vars[key])
                    #once loop it done write the line to the new per device config file
                    parsed_command_file.write(parsed_line)

#Main part to send configs
#open file with device configs (json)
with open(device_file) as json_file:
    #open the object in json
    reader = json.load(json_file)
    #loop through devices in json file
    for entry in reader['devices']:
        #print device entry
        print(entry)
        #define device dictionary to use for ConnectHandler
        device = {
        "device_type": entry['device_type'],
        "host": entry['host'],
        "username": username_input,
        "password": password_input,
        }
#initiate connection handler with all the variables from the device variable (dict) then send it commands
        with ConnectHandler(**device) as net_connect:
            #if yes to prechecks run through some show commands
            if prechecks == True:
                with open(prechecks_commands_file) as precheck_command_file:
                    for line in precheck_command_file:
                        output1 = net_connect.send_command(line);
# print outputs
                        print("\n" + output1 + "\n")
                        with open(device['host'] + "_log.txt", 'a') as log:
                            log.writelines(output1)
                prechecks = False
            #Main loop for config commands, checks if device_configs_commands is true
            if device_config_commands == True:
                with open(entry['hostname']+"_parsed_"+configure_commands_file) as parser_command_file:
                    #create a list for commands
                    commands = []
                    #loop through and merge variables into commands if present
                    for line in parser_command_file:
                        commands.append(line)
                    print(commands)
                    output2 = net_connect.send_config_set(commands)
    # print outputs
                    print("\n" + output2 + "\n")
                    with open(device['host'] + "_log.txt", 'a') as log:
                        log.writelines(output2)
                    #print(re.findall("(([Ff]*|[Gg]()).*[Ee]thernet...)",output1))
                    #print(re.findall(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",output1))
            #if yes to post checks run through some show commands
            if postchecks == True:
                with open(postchecks_commands_file) as postcheck_command_file:
                    for line in postcheck_command_file:
                        output2 = net_connect.send_command(line)
    # print outputs
                        print("\n" + output1 + "\n")
                        with open(device['host'] + "_log.txt", 'a') as log:
                            log.writelines(output1)
                postchecks = False
        #print("\n" + output2 + "\n")
