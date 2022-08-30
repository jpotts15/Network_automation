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
from paramiko import AuthenticationException

device_file = input("Enter device list filename (with json extension): ")
check = True
prechecks = False
device_config_commands = False
postchecks = False
#Prompt for file of commands to run before making changes
#Generic while loop used elsewhere so will explain here but not down the line

##Define Functions##
#ask yes/no Functions
def yes_no_question(question='this is the default yes/no question'):
    '''
    Function to provide yes/no question with some checking done
    '''
    #counter to error out after too many tries
    counter = 0
    #while loop to loop if bad input is taken in
    while True:
        #get input, set to lower and strip whitespace
        answer = input(f"{question} (y/n) [default y]: ").lower().strip()
        #if answer is no yes, also check length to make sure there is some input
        if len(answer) != 0 and answer[0] != 'y':
            #if answer is n/ no/ etc
            if answer[0] == 'n':
                return 'n'
                False
            #if not yes or no and counter is less then max increment counter and go back
            elif counter < 2:
                counter += 1
                continue
            #else condition for bad input and counter is over
            else:
                print("Error, too many tries")
                return "error"
                False
        #if yes then return y
        if len(answer) == 0 or answer[0] == 'y':
            return 'y'
            False

#define function to use yes/no and ask for file input
def yes_no_file_input(question="Default yes_no_file_input question", filename_question="Enter filename: "):
    '''
    This function asks a question then gets a file input and does some checking
    '''
    yes_no_file_input = yes_no_question(question)
    if yes_no_file_input == 'y':
        while True:
            yes_no_file_input_file = input(f"{filename_question} ")
            filename_check = yes_no_question(question=f"Is this the right filename {yes_no_file_input_file}")
            if len(yes_no_file_input_file) == 0:
                print("please enter the filename")
                continue
            if filename_check == 'y':
                return yes_no_file_input_file
                False

#ask if there are prechecks, configs and postchecks to run and get file input
prechecks_commands_file = yes_no_file_input(question="Do you have prechecks to run?",filename_question="Enter prechecks filename")
configure_commands_file = yes_no_file_input(question="Do you have config commands to run?",filename_question="Enter config commands filename")
postchecks_commands_file = yes_no_file_input(question="Do you have postchecks to run?",filename_question="Enter postchecks filename")

#put in username and password
username_input = input("Enter username: ")
password_input = getpass()

##config parser to replace variables in configs from json file
#open file with device configs (json)
if configure_commands_file != None:
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
try:
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
                if prechecks_commands_file != None:
                    with open(prechecks_commands_file) as precheck_command_file:
                        for line in precheck_command_file:
                            output1 = net_connect.send_command(line)
    # print outputs
                            print("\n" + output1 + "\n")
                            with open(device['host'] + "_log.txt", 'a') as log:
                                log.writelines(output1)
                    prechecks = False
                #Main loop for config commands, checks if device_configs_commands is true
                if configure_commands_file != None:
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
                if postchecks_commands_file != None:
                    with open(postchecks_commands_file) as postcheck_command_file:
                        for line in postcheck_command_file:
                            output2 = net_connect.send_command(line)
        # print outputs
                            print("\n" + output1 + "\n")
                            with open(device['host'] + "_log.txt", 'a') as log:
                                log.writelines(output1)
                    postchecks = False
            #print("\n" + output2 + "\n")

except AuthenticationException as err:
    print(f"Auth Failure: {err}")
except ConnectionRefusedError as err:
    print(f"Connection Refused: {err}")
except TimeoutError as err:
    print(f"Connection Timed out: {err}")
except Exception as err:
    exception_type = type(err).__name__
    print(f"Some other error occured: {exception_type}")
