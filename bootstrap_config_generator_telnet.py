#!/usr/bin/env python3
#imports
import telnetlib
from getpass import getpass
from time import sleep
#from netaddr import IPAddress

#Cisco bootstrap config generator
##this script will ask several basic questions and then output
##this script will require interactive reesponse, later will write one that inputs from file

##To improve add:
#everything to be wrote to file into a list and then iterate over that#
#def modules for reoccuring questions and create variables to subsitute in
#this version uses netmiko and telnet to send configs through telnet
#still making the script interactive so you can just go one by one through lab
#devices

##Setup variables##
hostname = ""
filename = ""
check = True
oobm_int = ""
oobm_int_ip = ""
oobm_int_ip_mask = ""
oobm_int_ip_mask_cidr = 0
username = ""
password = ""

####General Info####
##loop for hostname and domain as string with verficiation
check = True
while check == True:
	hostname = str(input("Enter device hostname: "))
	domain_name = str(input("Enter device domain name: "))
	print("Is {}, {} the correct hostname and domain".format(hostname,domain_name))
	#check response, make answer lower and strip to y or n
	hostname_check = str(input('Yes or No: )').lower().strip())
	if hostname_check[0] == 'y':
		check = False
	if hostname_check[0] != 'y':
		check = True

##loop for OOBM interface as string with verficiation
check = True
while check == True:
	oobm_int = str(input("Enter device OOBM Interface: "))
	print("Is {} the correct interface for the OOBM connection".format(oobm_int))
	#check response, make answer lower and strip to y or n
	oobm_int_check = str(input('(Yes or No: )').lower().strip())
	if oobm_int_check[0] == 'y':
		check = False
	if oobm_int_check[0] != 'y':
		check = True

##loop for OOBM interface IP as string with verficiation
check = True
while check == True:
	oobm_int_ip = str(input("Enter device OOBM Interface IP in dotted decimal (x.x.x.x) or enter \"DHCP\" for DHCP: ")).lower()
	if oobm_int_ip != 'dhcp':
		oobm_int_ip_mask = str(input("Enter device OOBM Interface subnet mask in dotted decimal (x.x.x.x): "))
		oobm_int_ip_mask_cidr = sum(bin(int(x)).count('1') for x in oobm_int_ip_mask.split('.'))
		print("Is {} {} the correct IP and mask".format(oobm_int_ip, oobm_int_ip_mask))
	else:
		print("Is DHCP correct for this interface?")
	#check response, make answer lower and strip to y or n
	oobm_int_ip_check = str(input('(Yes or No: )').lower().strip())
	#also create cidr from oobm_int_ip_mask
	if oobm_int_ip_check[0] == 'y':
		check = False
	if oobm_int_ip_check[0] != 'y':
		check = True




####End General Info####

####Vendor Specific Info####
#setup device type for specific questions
#device map
# device_type = 1 - Cisco
# device_type = 2 - Juniper

check = True
device_type = 0

while check == True:
	device_type = int(input("Enter 1 for Cisco and 2 for Juniper:"))
	if device_type == 1:
		#print("Cisco specific commands")
		##loop for username and password as string with verficiation
		check = True
		while check == True:
			username = str(input("Enter device username: "))
			print("Note: Enter a password placeholder only!")
			password = str(input("Enter password placeholder: "))
			print("Is {}, {} the correct username and password placeholder".format(username,password))
			#check response, make answer lower and strip to y or n
			username_check = str(input('Yes or No: )').lower().strip())
			if hostname_check[0] == 'y':
				check = False
			if hostname_check[0] != 'y':
				check = True
		check = False
	if device_type == 2:
		#print("Juniper specific commands")
		check = False

####End Vendor Specific Info####


####Write to file####
#set filename
filename = "bootstrap_config_" + hostname + ".txt"

#open/create new output file and write various lines to it
if device_type == 1:
	with open(filename,'w') as f:
		f.write("conf t")
		f.write("\n hostname " + hostname)
		f.write("\n interface " + oobm_int)
		if oobm_int_ip == 'dhcp':
			f.write("\n ip add dhcp")
		else:
			f.write("\n ip add " + oobm_int_ip + " " + oobm_int_ip_mask)
		f.write("\n no shut")
		f.write("\n exit")
		f.write("\n ip domain-name " + domain_name)
		f.write("\n username {} priv 15 password {}".format(username,password))
		f.write("\n crypto key generate rsa mod 2048")
		f.write("\n line vty 0 15")
		f.write("\n transport input ssh")
		f.write("\n login local")
		f.write("\n end")
		f.write("\n write")
		f.write("\n")
		f.write("\n")
		f.write("\n show ip int bri")


if device_type == 2:
	with open(filename,'w') as f:
		f.write("\n cli")
		f.write("\n configure")
		f.write("\n set system login user admin authentication plain-text-password")
		f.write("\n set system root-authentication plain-text-password")
		f.write("\n set system login user admin class super-user")
		f.write("\n delete chassis auto-image-upgrade")
		f.write("\n set system host-name " + hostname)
		if oobm_int_ip == 'dhcp':
			f.write("\n set interfaces " + oobm_int + " unit 0 family inet dhcp")
		else:
			f.write("\n set interfaces " + oobm_int + " unit 0 family inet address " + oobm_int_ip + "/" + str(oobm_int_ip_mask_cidr))
		f.write("\n commit")


print("Config generations successful, filename {}".format(filename))

#Send to device config
send_to_device = input("Use telnet to send to device? (y/n): ").lower().strip()

if send_to_device[0] == 'y':
	#need to split out cisco vs juniper as bootstrap behavior is different
	if device_type == 1:
		telnetport = input("input telnet port number: ")
		tn = telnetlib.Telnet("192.168.2.15", telnetport)
		sleep(5)
		tn.write(b"\r\n")
		tn.write(b"no\r\n")
		tn.write(b"\r\n")
		sleep(20)
		tn.write(b"en\r\n")
		with open (filename, 'r') as telnet_file:
			for line in telnet_file:
				tn.write(line.encode('ascii') + b"\r\n")
				sleep(1)
			tn.write(b"exit\r\n")
		print("sending complete!")
	if device_type == 2:
		telnetport = input("input telnet port number: ")
		tn = telnetlib.Telnet("192.168.2.15", telnetport)
		sleep(5)
		tn.write(b"\r\n")
		tn.write(b"\r\n")
		sleep(5)
		with open (filename, 'r') as telnet_file:
			for line in telnet_file:
				tn.write(line.encode('ascii') + b"\r\n")
				sleep(1)
			tn.write(b"exit\r\n")
		print("sending complete!")
if send_to_device[0] != 'y':
	print("File saved but not sent, exiting!")
#print(tn.read_all().decode('ascii'))
