#!/usr/bin/env python3
import json

#script based off my other netmiko scripts
#this will take a input file for devices and variables (json) and a input file for commands
#then parse them together in a per device config

#enter file names
device_file = input("Enter device list filename (with json extension): ")
configure_commands_file = input("Enter configure commands filename: ")

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
            print('Done parsing file ' + json_device_entries["hostname"]+"_parsed_"+configure_commands_file)