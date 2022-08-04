#!/usr/bin/env python3
from netmiko import ConnectHandler
from getpass import getpass

#derived from https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md
#example Executing show command and mutli devices

#put in username and password
username_input = input("Enter username: ")
password_input = getpass("Enter password: ")
secret_input = getpass("Enter enable password/secret: ")

#Add list to be a list of devices
devices = []
devices_parameters = []

#define devices as a dictionary
cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.2.179",
    "username": username_input,
    "password": password_input,
    "secret" : secret_input,
}
cisco1_parameters = {
    "int1" : "gi0/0",
    "int1_ip": "10.10.0.1",
    "int1_ip_mask" : "255.255.255.252",
}
#Append this device to a list of devices
devices.append(cisco1)
devices_parameters.append(cisco1_parameters)

#repeat for more devices
cisco2 = {
    "device_type": "cisco_ios",
    "host": "192.168.2.181",
    "username": username_input,
    "password": password_input,
    "secret" : secret_input,
}
cisco2_parameters = {
    "int1" : "fa0/0",
    "int1_ip": "10.10.0.2",
    "int1_ip_mask" : "255.255.255.252",
}
devices.append(cisco2)
devices_parameters.append(cisco2_parameters)

#loop over the list of devices with each to initiate connection handler with
#all the variables from the device variable (dict) then send it commands
for device_parameter in devices_parameters :
    print(device_parameter)
    for device in devices:
        print(device)
        # Show commands that we will run
        config_command1 = []
        config_command1.append("conf t")
        config_command1.append("int " + device_parameter['int1'])
        config_command1.append("ip add  " + device_parameter['int1_ip'] + " " + device_parameter['int1_ip_mask'])
        config_command1.append("no shut")
        config_command1.append("end")
        print(config_command1)
        show_command1 = "show ip int brief"
        show_command2 = "show ip route"
        with ConnectHandler(**device) as net_connect:
            #net_connect.enable()
            config1 = net_connect.send_config_set(config_command1)
            output1 = net_connect.send_command(show_command1)
            output2 = net_connect.send_command(show_command2)

    # print outputs inside the loop
        print("Output of " + device["host"] + "\n" + output1 + "\n")
        print("Output of " + device["host"] + "\n" + output2 + "\n")
