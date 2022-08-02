# Network_automation
This repo will house various network automation scripts, playbooks, etc

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

**Boot Strap Configs**

Boot strap configs will build IP reachability to an machine external to the lab which will run various automations. These configs will include:
1. Configure hostname, domain and generate SSL certs (if required) - doing this manually to enable ssh
2. OOBM interface configured for DHCP and put in management VRF
3. Allow SSH access to a specific IP for the external automation host
4. Verify network reachability 

**Python Automation**

![python_automation_diagram](https://user-images.githubusercontent.com/110405079/182413710-9bbd0026-b152-4cbc-8409-87d212860ab4.PNG)

Diagram above shows the devices to be configured using python
