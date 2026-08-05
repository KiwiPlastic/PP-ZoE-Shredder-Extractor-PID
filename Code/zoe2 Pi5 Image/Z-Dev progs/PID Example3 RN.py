
#=========================================================================
# Ver 0.4 from PID example2.py
#
# Date:16-8-2020
#
# Development/learning project
# - 3 x PID Temperature controlers for Precious Plastic ZoE(Zherdder or Extruder combo machine)
#
#
# Goals:
#
# - 3 x SPI temperture sensors, K type termocouple - Done
# - 3 x PID control loops for each temperature sensor - 1 x done
# - 3 x GPIO outputs for SSR + Band Heaters
# - User interface input fuctions (Target Temp, PID values) - Done
# - graphs
# - GUIZERO interface
# - logging Temps and Output
# - Touch screen
#
# Status: 18-8-20
# Reads 3 x MAX667 SPI Thermocoupls
# Has Shell Input of PID values and uses a default value  if ENTER pressed at Shell input line
# if temperature1 is less than target by n DegC then Ramp up the Heat, turn output on
# Goes into PID loop, draws real time graph
# writes csv file to disk
#
# work stopped due to issues with mutil traces on graphs ......
# ...this method does not work for real time data. Use Obgect Orientated approch  
#
#==========================================================================


import os
#import time
from time import sleep, strftime, time
import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675
import matplotlib.pyplot as plt
#from gpiozero import CPUTemperature
#cpu = CPUTemperature()

#fig, ax1 = plt.subplots()
        
#--------------------------------------------------------------------
# subrotines
#--------------------------------------------------------------------

#------------------------- Write Data to disk -----------------------
def write_temp(temp1, temp2, temp3):
    
    with open("/home/pi/Documents/Python/Zoe_temps.csv", "a") as log:
        log.write("{0},{1},{2},{3}\n".format(strftime("%y-%m-%d %H:%M:%S"),str(temp1),str(temp2),str(temp3)))
        
#-------------------------- Plot Data on Graph ---------------------
def graph(data1):
        y.append(data1)
        x.append(time())
        plt.clf() 
        plt.title('Sensor 1')
        plt.xlabel('Time')
        plt.ylabel('Temperature DegC')
        plt.ylim(0,40)
        plt.scatter(x, y)
        plt.plot(x, y)
        plt.draw()

#------------- turn the PID output on/off (Heater Element on GPIO pin) -----
def turn_on():
  os.system("sudo ./strogonanoff_sender.py --channel 4 --button 1 --gpio 0 on")

def turn_off():
  os.system("sudo ./strogonanoff_sender.py --channel 4 --button 1 --gpio 0 off") 

#-------------- read 3 x SPI Temperature Sensors in Deg C -------------------
def tempdata():
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3
    
#---------------------------------------------------------------------------------
# We need to read 3 x Thermocpule temperatures from 3 x MAX6675 chip which are
# on the SPI bus. The MAX6675 uses chip select lines to activate each chip.
#
# MAX6675 SPI Temperature function, what can be passed to this and read from it?
#
# sensor = MAX6675.MAX66&5(CLK, CS, DO, SPI, GPIO)
# temp = sensor.readTempC()
# tempbuf = sensor.read16()
#
# PIN numbering is GPIO not Pcb Header
#
# CLK = 14 clock GPIO pin to be used 
# CS1  = 2 Chip Select GPIO pin to be used
# CS2 = 3
# CS3 = 4
# DO  = 18 Data in from Thermocuple into GPIO pin to be used
# SPI = Not being used. selects hardware SPI see example. No CS hardware does it, unles you Use GPIO pins an ctrl yourself
# GPIO = Not being used. selects GPIO pin numbers(default) or pcb
# 
# Software SPI gives better control on chip select, for more than two SPI devices
#===============================================================================

# Raspberry Pi software SPI configuration.

CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

#-----------------------------------------------------
# Get PID inputs
target = input('Enter Target Temperature, DegC : ')
if (target==""):
  target = 28
target = int(target)
print ('Target Temperature is: %d' % (target))
print ()

P = input('Enter P value: ')
if (P==""):
  P = 1
P = int(P)
print ('P = ',P)
print ()

I = input('Enter I value: ')
if (I==""):
   I = 1
I = int(I)
print ('I = ',I)
print ()

D = input ('Enter I value: ')
if (D==""):
  D = 0
D = int(D)
print ('D = ',D)
print ()

# at start up it might require a Temperature ramp up to get with in target Temp
# If target-temperature > targetdif, DegC
print ('Set Ramp up trigger temperature Deg C')
print (' ie if Startup Temp is n Deg C less than Target Temp, turn output on')
targetdif = input ('Enter Ramp startup value : ')
if (targetdif==""):
  targetdif = 6
targetdif = int(targetdif)
print ('targetdif = ',targetdif)
print ()

# Initialise some variables 
interror = 0

plt.close('all')
plt.ion()
x=[]
y=[]

# Turn on for initial ramp up
state="on"
turn_on()

#read initial temperature values for Ramp up
[Temp1, Temp2, Temp3] = tempdata()
print ('Thermocouple Temperatures: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(Temp1, Temp2, Temp3))
temperature = Temp1 # load PID sensor variable
print("Output is ON. For Initial Temperature Ramp up")
while (target - temperature > targetdif):
    print('{0:0.2F} C {1:0.2F} C'.format(temperature, target))
    sleep(5)
    [Temp1, Temp2, Temp3] = tempdata()
    temperature = Temp1
    

#----------------------------------------------------------
# event loop
#----------------------------------------------------------


print("**********Entering PID control loop****************")
while True:
    [Temp1, Temp2, Temp3] = tempdata()
    temperature=Temp1
    error = target - temperature
    interror = interror + error
    power = D + ((P * error) + ((I * interror)))

    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(Temp1, Temp2,Temp3))
    print ()
    print ("TARGET TEMP =",target)
    print ()
    print ("P =",P)
    print ("I =",I)
    print ("D =",D)
    print ()
    print ("Error = target - temp =", error)
    print ("Int Error = Int error + Error =",interror)
    print ()
    print ('Output on if > 10')
    print ("Power Output =", power)
    print ()

    # Make sure that if power should be off then it is
    if (state=="off"):
        turn_off()
        print ("Pwr saftey set to Off")
        print ()
    #if power > than base PID values turn output ON.  else turn output OFF
    if (power>10  ):
        print ("PID power ON")
        print()
        state="on"
        turn_on()
    else:
        print ("PID power OFF")
        print ()
        state="off"
        turn_off()

    print ("state=", state)
    print ("=============================")


    write_temp(Temp1, Temp2, Temp3)     #write temperature data to disk
    graph(temperature)                                   # update graph
    plt.pause(1)                                                # pause the graph else no update
   
    sleep(2)
    

