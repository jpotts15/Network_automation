#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass
import json

#derived from my previous netmiko scripts
#this is slightly different version of the netmiko_config_devices_from_json.py but instead of taking in check/config files
#it assumes the input json file has a file parameter in it and then uses that per device

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
        postchecks = True
        check = False
    if postchecks_check[0] != 'y':
    	check = False

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

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
            device_vars = entry['vars']
            #if yes to prechecks run through some show commands
            if prechecks == True:
                with open(device_vars['prechecks']) as precheck_command_file:
                    for line in precheck_command_file:
                        output1 = net_connect.send_command(line);
# print outputs
                        print("\n" + output1 + "\n")
                        with open(device['host'] + "_log.txt", 'a') as log:
                            log.writelines(output1)
                prechecks = False
            #Main loop for config commands, checks if device_configs_commands is true
            if device_config_commands == True:
                with open(device_vars['configs']) as parser_command_file:
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
                with open(device_vars['postchecks']) as postcheck_command_file:
                    for line in postcheck_command_file:
                        output2 = net_connect.send_command(line)
    # print outputs
                        print("\n" + output1 + "\n")
                        with open(device['host'] + "_log.txt", 'a') as log:
                            log.writelines(output1)
                postchecks = False
        #print("\n" + output2 + "\n")
