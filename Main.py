import Configuration as conf
import Common_Functions as cf
import sys
import time

# Connect to Wi-Fi
if(conf.option == 0):
    i = conf.connection_time
    while(i>=1):
        k = cf.connect_network(conf.SSID)
        if(k):
            i=0
            cf.is_connected()
        else:
            i-=1
# Create a open Wi-Fi profile and connect to it.
elif(conf.option == 1):
    cf.openwifi(conf.SSID)
# Create a secured Wi-Fi profile and connect to it.
elif(conf.option == 2):    
    cf.securedwifi(conf.SSID,conf.password)
# Delete Wi-Fi profile.
elif(conf.option == 3):
    cf.delete_profile(conf.SSID)
# Edit Profile.
# If profile is open password value be None.
elif(conf.option == 4):
    cf.edit_profile(conf.SSID, conf.password, conf.Profile_type)