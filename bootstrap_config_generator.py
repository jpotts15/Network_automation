#!/usr/bin/env python3
#imports
#from netaddr import IPAddress

#Cisco bootstrap config generator
##this script will ask several basic questions and then output
##this script will require interactive reesponse, later will write one that inputs from file

##To improve add:
#everything to be wrote to file into a list and then iterate over that#
#def modules for reoccuring questions and create variables to subsitute in

##Setup variables##
hostname = ""
filename = ""
check = True
oobm_int = ""
oobm_int_ip = ""
oobm_int_ip_mask = ""
oobm_int_ip_mask_cidr = 0

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
		f.write("\n crypto key generate rsa mod 2048")
		f.write("\n end")
		f.write("\n write")
		f.write("\n show ip int bri")


if device_type == 2:
	with open(filename,'w') as f:
		f.write("\n configure")
		f.write("\n set system login user admin authentication plain-text-password")
		f.write("\n set system login user admin class super-user")
		f.write("\n set host-name " + hostname)
		f.write("\n set interfaces " + oobm_int + " unit 0 family inet address " + oobm_int_ip + "/" + str(oobm_int_ip_mask_cidr))
		f.write("\n commit")


print("Config generations successful, filename {}".format(filename))
