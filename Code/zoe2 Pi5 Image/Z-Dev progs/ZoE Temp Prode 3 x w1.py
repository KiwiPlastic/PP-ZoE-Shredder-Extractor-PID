#!/usr/bin/env python

# ZoE test Temperature probe Program - 1 wire, 3 sensors

import os
import glob
import time
import datetime


new_temp1 = 1.2
new_temp2 = 2.2
new_temp3 = 3.3

"""Reads the temperature from a 1-wire device SN 28-****"""
temperature1 = glob.glob("/sys/bus/w1/devices/" + "28-000000784af1")[0] + "/w1_slave"
temperature2 = glob.glob("/sys/bus/w1/devices/" + "28-0000007252a4")[0] + "/w1_slave"
temperature3 = glob.glob("/sys/bus/w1/devices/" + "28-000000784012")[0] + "/w1_slave"


#==============================================
def read_temperature1(decimals = 1):
    global new_temp1
    try:
        with open(temperature1, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            new_temp1 = round(float(temp_string) / 1000.0, decimals)
            return (new_temp1)            
    except Exception:
        pass
    
#====================================================    
def read_temperature2(decimals = 1):
    global new_temp2
    try:
        with open(temperature2, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            new_temp2 = round(float(temp_string) / 1000.0, decimals)
            return (new_temp2)
    except Exception:
        pass  

#====================================================    
def read_temperature3(decimals = 1):
    global new_temp3
    try:
        with open(temperature3, "r") as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            new_temp3 = round(float(temp_string) / 1000.0, decimals)
            return (new_temp3)
    except Exception:
        pass
    
#==========================================================
# Event Loop printing measurements every second
print ('Press Ctrl-C to quit.')    
while True:
    read_temperature1()
    print (new_temp1)
    read_temperature2()
    print (new_temp2)
    read_temperature3()
    print (new_temp3)
    time.sleep(1.0)
 