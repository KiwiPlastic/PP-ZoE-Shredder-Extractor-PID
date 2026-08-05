#!/usr/bin/env python

# ZoE (Shreder of Extruder)
# v19 17-11-25
#
#==================================================================
# GPIO H/W pin assignment, using GPIO(BCM) labeling
# GPIO 0  (ID_SD)
# GPIO 1  (ID_SC)
# GPIO 2  (I2C SDA)   		
# GPIO 3  (I2C SCL)  		
# GPIO 4  (GP CLK0)  	            - 1-Wire Temperature Probe  I/O
# GPIO 5				            - Opto Coupler 1 			IP
# GPIO 6				            - Opto Coupler 2 			IP
# GPIO 7  (SPI0 CE1)				- 
# GPIO 8  (SPI0 CE0)				- 
# GPIO 9  (SPIO MISO)
# GPIO 10 (SPI0 MOSI)
# GPIO 11 (SPI0 SCLK)
# GPIO 12 (PWM0)
# GPIO 13 (PWM1)
# GPIO 14 (TXD) 		
# GPIO 15 (RXD) 		
# GPIO 16 (SPI1 CE2)				
# GPIO 17 (SPI1 CE1)			
# GPIO 18 (SPI1 CE0 PCM_CLK)		
# GPIO 19 (SPI1 MISO PCM_FS)	    
# GPIO 20 (SPI1 MOSI PCM_DIN)
# GPIO 21 (SPI1 SCLK PCM_DOUT)		
# GPIO 22  				            - Heater 1   			    OP
# GPIO 23  				            - Heater 2  			    OP
# GPIO 24 				            - Heater 3				    OP
# GPIO 25  				            - Alarm Pizo	  		    OP
# GPIO 26				            - Emergency Shutdown 	    IP
# GPIO 27  				 			
#================================================================

from time import strftime           # used to write data to disk
from time import sleep
#import datetime as dt
import os, sys
#import os
#import select						# keyboard input for CLI

#Load code from files
import Zoe_Sensors
import Zoe_Outputs
import Zoe_ConfigFile
import Zoe_PID
import Zoe_CLI
import Zoe_Reset
import Zoe_Help_text

#import Zoe_Init_GUI
#import Zoe_GUI
#import Zoe_Events
#import Zoe_Bindings
#import Zoe_Animate



#=====================================================



#====================================================
#               INIT Global VARIABLES 
#====================================================

# Calibration Parameters
pwr_op_on = 10              # PID power base line must get above to turn on
pwr_op_alm_limit = 100      # Max value PID ouput will get to before alarm shut down ( Heater not working)
preheat_trig = 5            # Target_Temp - preheat_trig = n If temp > n do pidautorun if on
pidautorun = 1              # After preheat turn PIDs on else makes alram

# Initialise PID variables 
target1 = 27
P1 = 1.0
I1 = 1.0
D1 = 0.0
interror1 = 0
error1 = 0
power1 = 0

target2 = 28
P2 = 1.0
I2 = 1.0
D2 = 0.0
interror2 = 0
error2 = 0
power2 = 0

target3 = 29
P3 = 1.0
I3 = 1.0
D3 = 0.0
interror3 = 0
error3 = 0
power3 = 0

# file handeling tags
filename = ""
open_folder = "/home/richn/zoe2/Data"
open_defaults_file = True           #set to false to use hard coded values from above

# Global variable to remember various states
PID1_run_state = False
PID2_run_state = False
PID3_run_state = False
manual_state = False
heater1_state = False
heater2_state = False
heater3_state = False
PID1_alarm_state = False
PID2_alarm_state = False
PID3_alarm_state = False
preheat1_state = False
preheat2_state = False
preheat3_state = False
pizo_state = False

# Temperature probe values
new_temp1 = 1.2
new_temp2 = 2.2
new_temp3 = 3.3

#====================================================
# Event Loop printing measurements every second
print ('Press q to quit.')    
while True:
    #get key board input
    Zoe_CLI.cmd()
    
    # Read Tempeatures
    Zoe_Sensors.read_temperature1()
    print (Zoe_Sensors.new_temp1)
    
    Zoe_Sensors.read_temperature2()
    print (Zoe_Sensors.new_temp2)
    
    Zoe_Sensors.read_temperature3()
    print (Zoe_Sensors.new_temp3)

    #read Emergancy Shut down Push Button
    Zoe_Sensors.Read_ES_PB()
    
    #Turn Output On/Off
    Zoe_Outputs.heater1(heater1_state)
    heater1_state = not(heater1_state)
 
    Zoe_Outputs.heater2(heater2_state)
    heater2_state = not(heater2_state)
    
    Zoe_Outputs.heater3(heater3_state)
    heater3_state = not(heater3_state)
    
    Zoe_Outputs.alarm_pizo(pizo_state)
    pizo_state = not(pizo_state)
 
#sleep(1.0)
 