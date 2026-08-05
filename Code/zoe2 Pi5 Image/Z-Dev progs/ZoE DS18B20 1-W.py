#!/usr/bin/env python

# ZoE test Temperature test Program 1 wire, 3 sensors

import os
import glob
import time
import datetime

def read_temp(decimals = 1, sleeptime = 1):

    """Reads the temperature from a 1-wire device"""

    temperature1 = glob.glob("/sys/bus/w1/devices/" + "28-000000784af1")[0] + "/w1_slave"
    temperature2 = glob.glob("/sys/bus/w1/devices/" + "28-0000007252a4")[0] + "/w1_slave"
    temperature3 = glob.glob("/sys/bus/w1/devices/" + "28-000000784012")[0] + "/w1_slave"
    
    while True:
        try:
            timepoint = datetime.datetime.now()
            with open(temperature1, "r") as f:
                lines = f.readlines()
            while lines[0].strip()[-3:] != "YES":
                time.sleep(0.2)
                lines = read_temp_raw()
            timepassed = (datetime.datetime.now() - timepoint).total_seconds()
            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp = round(float(temp_string) / 1000.0, decimals)
                print(time.strftime("Temperature1 %d/%m/%y@%H:%M:%S - ")+str(temp)+" C")
                time.sleep(sleeptime-timepassed)
                timepoint = datetime.datetime.now()
                
            with open(temperature2, "r") as f:
                lines = f.readlines()
            while lines[0].strip()[-3:] != "YES":
                time.sleep(0.2)
                lines = read_temp_raw()
            timepassed = (datetime.datetime.now() - timepoint).total_seconds()
            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp = round(float(temp_string) / 1000.0, decimals)
                print(time.strftime("Temperature2 %d/%m/%y@%H:%M:%S - ")+str(temp)+" C")
                time.sleep(sleeptime-timepassed)
                timepoint = datetime.datetime.now()
            
            with open(temperature3, "r") as f:
                lines = f.readlines()
            while lines[0].strip()[-3:] != "YES":
                time.sleep(0.2)
                lines = read_temp_raw()
            timepassed = (datetime.datetime.now() - timepoint).total_seconds()
            equals_pos = lines[1].find("t=")
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp = round(float(temp_string) / 1000.0, decimals)
                print(time.strftime("Temperature3 %d/%m/%y@%H:%M:%S - ")+str(temp)+" C")
                time.sleep(sleeptime-timepassed)
                timepoint = datetime.datetime.now()
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    read_temp()