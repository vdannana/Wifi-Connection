import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import Configuration as conf


# Create a Open Wifi Profile and connect to it.
def openwifi(SSID):
    pname = create_open_profile(SSID)
    addProfile(pname)
    time.sleep(2)
    result = connect_network(SSID)
    time.sleep(5)
    print_Wifi_details()


# Create a Secred Wifi Profile and connect to it.
def securedwifi(SSID,password):
    pname = create_secure_profile(conf.SSID,conf.password)
    addProfile(pname)
    time.sleep(2)
    result = connect_network(conf.SSID)
    time.sleep(3)
    print_Wifi_details()


# Converting String to Hexadecimal value
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)    
    str1 = ""  
    for ele in lst:  
        str1 += ele
    return str1


# Adding created profile to the saved Wi-Fi profiles 
def addProfile(fname):
    command = "netsh wlan add profile filename=\""+fname+"\""
    print(command)
    output = subprocess.run(command)
    if(output.returncode != 0):
        print(output.stdout)
        exit(0)
    else:
        print('Profile ' + fname + ' is added')


# Print Connected Wi-Fi Detalils
def print_Wifi_details():
    command = 'netsh wlan show interfaces'
    output = subprocess.run(command, shell=True)


# Connecting to the Wi-Fi.
def connect_network(iname):
    command = 'netsh wlan connect name="' + iname
    output = subprocess.run(command, capture_output=True, text=True)
    # Check if system reconnect to same network successfully.
    if output.returncode != 0:
        print(output.stdout)
        exit(0)
    else:
        print(output.stdout)


# Creats open wifi profile.
def create_open_profile(iname):
    cpname = conf.Output_Folder + '/' + "Wi-Fi-" + iname + ".xml"
    f = open(cpname, "w")    
    with open(conf.Open_Profile_File,"r") as fi:
        for line in fi:
            if(re.search("^\t<name>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 7):
                        string = string + iname
                f.write(string)
            elif(re.search("^\t\t\t<name>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 9):
                        string = string + iname
                f.write(string)
            elif(re.search(".*<hex>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 8):
                        string = string + toHex(iname)
                f.write(string)
            else:
                f.write(line)
    f.close()  
    print("Profile " + cpname + " is created")  
    return cpname


# Creats secured wifi profile.
def create_secure_profile(iname,password):
    cpname = conf.Output_Folder + '/' + "Wi-Fi-" + iname + ".xml"
    print(cpname)
    f = open(cpname, "w")    
    with open(conf.Secured_Profile_File,"r") as fi:
        for line in fi:
            if(re.search("^\t<name>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 7):
                        string = string + iname
                f.write(string)
            elif(re.search("^\t\t\t<name>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 9):
                        string = string + iname
                f.write(string)
            elif(re.search(".*<hex>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 8):
                        string = string + toHex(iname)
                f.write(string)
            elif(re.search(".*<keyMaterial>.*", line)):
                string = ""
                count=0
                for e in line:
                    count+=1
                    string = string + e
                    if(count == 17):
                        string = string + password
                f.write(string)    
            else:
                f.write(line)
    f.close()  
    print("Profile " + cpname + " is created")  
    return cpname


# Delete Wifi profile from Saved Wifi profiles list
def delete_profile(iname):
    command = 'netsh wlan delete profile "' + iname +'"'
    print(command)
    output = subprocess.run(command, capture_output=True, text=True)
    # Check if system reconnect to same network successfully.
    if output.returncode != 0:
        print(output.stdout)
        return False
    else:
        print(output.stdout)


# Edit existing Wifi profile
def edit_profile(SSID, password, type):
    delete_profile(SSID)
    if(type == 0):
        openwifi(SSID)
    elif(type == 1):
        securedwifi(SSID, password)
