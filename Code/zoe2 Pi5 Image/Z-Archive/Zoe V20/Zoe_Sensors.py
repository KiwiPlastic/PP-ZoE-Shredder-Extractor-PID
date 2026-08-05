# ZoE: Measures all sensor inputs

import glob
import RPi.GPIO as GPIO

OPTO1_PIN 		= 5				# Encoder Opto1 Interupter IP
OPTO2_PIN 		= 6				# Encoder Opto2 Interupt IP

ES_PB_PIN = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ES_PB_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)

"""Reads the temperature from a 1-wire (GPIO4) device SN 28-****"""
temperature1 = glob.glob("/sys/bus/w1/devices/" + "28-000000784af1")[0] + "/w1_slave"
temperature2 = glob.glob("/sys/bus/w1/devices/" + "28-0000007252a4")[0] + "/w1_slave"
temperature3 = glob.glob("/sys/bus/w1/devices/" + "28-000000784012")[0] + "/w1_slave"

new_temp1 = 0
new_temp2 = 0
new_temp3 = 0

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
            print (new_temp1)
    except Exception:
        print ("Temp 1 w1 Failled")
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
        print ("Temp 2 w1 Failled")
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
        print ("Temp 3 w1 Failled")
        pass
    
#====================================================
def read_es_pb():
    global emergancy_stop
    try:
        emergancy_stop = False
        if GPIO.input(ES_PB_PIN) == GPIO.LOW:
            emergancy_stop = True
            print ("EMERGANCY STOP")
            return (emergancy_stop)
    except Exception:
        print ("ES Fail")
        pass
        
#====================================================
def encoder():
    print ("Rotary Encoder")
    