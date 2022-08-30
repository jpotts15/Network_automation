# Network_automation
This repo will house various network automation scripts, playbooks, etc.

I'll probably parse this down and port to the wiki for some info but leaving as is for now. 

I have a habit of learning new things, doing it once then moving on and forgetting and misplacing things so the intent with this repo is to help me store for network automation related scripts, playbooks, etc for later use. 

**Goal**

1. Build out a simple EVE-NG lab
2. Build simple boot strap type configs to gain reachability to virtual devices 
3. Use python with various modules to configure several devices
4. Use Ansible using various playbooks/methods to configure several different devices

**Requirements**

1. Build simple but reproducable scripts that are easily reread
2. Build things in a way that is similar to production networks, i.e. no telnet or using EVE-NG backdoors

**Overall Network Diagram**

![overall_network_diagram](https://user-images.githubusercontent.com/110405079/182412840-ec67553d-2c30-4008-85e5-c1b855d076da.PNG)

I originally was planning a lab for Cisco SPCOR study which is why its a service provider like network but wanted to shortcut some network automation learning so reusing this for now. 

**Boot Strap Config Generator**

Boot strap configs will build IP reachability to an machine external to the lab which will run various automations. These configs will include:
1. Configure hostname, domain and generate SSL certs (if required) - doing this manually to enable ssh
2. OOBM interface configured for DHCP and put in management VRF
3. Allow SSH access to a specific IP for the external automation host
4. Verify network reachability

Since this is about automation I thought why not write a config generator but as always there are a lot of little issues so this took a bit. The code probably could be better but I'm happy with the results for now. 

I've also added a hook to send this bootstrap via telnet so that with EVENG/GNS3 you can use that as sort of a management OOBM to bootstrap

**Python Automation**

![python_automation_diagram](https://user-images.githubusercontent.com/110405079/182413710-9bbd0026-b152-4cbc-8409-87d212860ab4.PNG)

Diagram above shows the devices to be configured using python

**Netmiko Scripts** 
There are a number of scripts that ramp up in complexity.

1. Netmiko_gather_info.py - Basic script that connects to a single device, runs some show commands and then prints the output of the commands
2. Netmiko_gather_info_multi.py - Same as #1 except runs against multiple devices hard coded into script
3. Netmiko_gather_info_csv.py - Same as #2 except imports devices from a csv file
4. Netmiko_configure_devices.py - New line of script but branches from #2 and runs some config commands as well as show commands
5. Netmiko_configure_devices_from_file.py - Basically a merge of #4 and #3, devices from CSV but loads list of configs from file
6. napalm_show_commands.py - Uses napalm to run some show commands

**Netmiko_config_devices_from_json.py**
This is where I've spent a lot of time building out something useful. Its the build up of the others with new things layered on. 

**Features**
Takes a json file input for devices(devices.json example), take in .txt file for commands (config_commands.txt example). 

Per device configuration can be done by adding variables into the config and then adding the corresdponing variable into the devices file under the appropriate device with the correct key/value pair. For instance in my toopology I added ibgp between two routers, for each device in devices.json I added "ibgp_int_ip": "172.16.0.1" and then added ibgp_int_ip as a variable of sorts to the config so that the config line looks like ip add ibgp_int_ip ibgp_int_mask.

Limitations:
1. Currently variables have to be unique and not parse to match another, for instance if you have the variable ibgp and then ibgp_int the ibgp variable would match both - Need to fix by changing the way replacement is done in the script

**Netmiko_config_devices_improved.py**
Next iteration of last script using actual function definitations and reuse. 

**eveng_api.py**
I started to work on a EVE-NG frontend so that I could quickly call a script to grab the telnet IP/Port for devices and input that into other scripts. Ran into some trouble w/ the telnet link so backburner now, there is another repo called EVENG-API that already does this so will likely just use that but still using this as a simple API example
