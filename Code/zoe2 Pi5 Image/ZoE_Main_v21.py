#!/usr/bin/env python
''''
# ZoE (Shreder of Extruder)
# v21 29-11-25
# For Pi5B using SPI Max6675 K Type thermocouple 0-1024 deg c 

TO DO
 Encode Dev code - inputs r working
 heater control pulsed
 plot, like clipper, basic +

# COMMANDS
# q         Quit
# ?         Help
# l         Load config file
# s         Save config file
# d         Load Defaults (reset)
# k         Kill - Shutdown pizo, Heaters and PIDs OFF
# p         Pizo On/Off Toggel
#
# r1        Run PID 1 Toggel On/Off
# t1=nn.n   Target Temperature PID 1 Target Degq
# p1=n.n    P PID 1 value 
# i1=n.n    I PID 1 value
# d1=n.n    D PID 1 value
# ...
#
# h1        Heater 1 On/Off Toggel
# h2        Heater 2 On/Off Toggel
# h3        Heater 3 On/Off Toggel
#
#==================================================================
# GPIO H/W pin assignment, using GPIO(BCM) labeling
# GPIO 0  (ID_SD)
# GPIO 1  (ID_SC)
# GPIO 2  (I2C SDA)   
# GPIO 3  (I2C SCL)  
# GPIO 4  (GP CLK0)                 -
# GPIO 5                  - Opto Coupler 1   IP
# GPIO 6                  - Opto Coupler 2   IP
# GPIO 7  (SPI0 CE1)
# GPIO 8  (SPI0 CE0)
# GPIO 9  (SPIO MISO)
# GPIO 10 (SPI0 MOSI)
# GPIO 11 (SPI0 SCLK)
# GPIO 12 (PWM0)
# GPIO 13 (PWM1)
# GPIO 14 (TXD) 
# GPIO 15 (RXD) 
# GPIO 16 (SPI1 CE2)    - Temperature3 Max 6675
# GPIO 17 (SPI1 CE1)    - Temperature2 Max 6675
# GPIO 18 (SPI1 CE0)    - Temperature3 Max 6675
# GPIO 19 (SPI1 MISO)   - Max 6675 - DO
# GPIO 20 (SPI1 MOSI)
# GPIO 21 (SPI1 SCLK)   - Max 6675 - CLK
# GPIO 22               - Heater 1       OP
# GPIO 23               - Heater 2       OP
# GPIO 24               - Heater 3       OP
# GPIO 25               - Alarm Pizo     OP
# GPIO 26               - Emergency Shutdown    IP
# GPIO 27 
#================================================================
'''

#import sys
#from sys import stdout       # This and the import below allow error signal reading to be displayed continuously on command line
import time
from time import sleep
from datetime import datetime

#import matplotlib.pyplot as plt
#import numpy as np

#Load code from files
import Zoe_Sensors        
import Zoe_Outputs
import Zoe_CLI
import Zoe_Help_text
import Zoe_ConfigFile

#====================================================

# call to Zoe_ConfigFile.py to init variabls
Zoe_ConfigFile.init()

#PID output
power1 = 0
power2 = 0
power3 = 0

# PID power1 > Threshold = Heater relay on
Threshold1 = 3
Threshold2 = 3
Threshold3 = 3

# this is to do with Plot
#plottime = np.linspace(0, 10, 100)  # 10 seconds, 100 steps this is used by plot
#process_values = []


#========================================================
class PID1:

   def __init__(self, p_gain, i_gain, d_gain, now):
      self.last_error = 0.0
      self.last_time = now

      self.p_gain = p_gain
      self.i_gain = i_gain
      self.d_gain = d_gain

      self.i_error = 0.0

   def Compute(self, input, target, now):
      dt = (now - self.last_time)

      #---------------------------------------------------------------------------
      # Error is what the PID alogithm acts upon to derive the output
      #---------------------------------------------------------------------------
      error = target - input

      #---------------------------------------------------------------------------
      # The proportional term takes the distance between current input and target
      # and uses this proportially (based on Kp) to control the ESC pulse width
      #---------------------------------------------------------------------------
      p_error = error

      #---------------------------------------------------------------------------
      # The integral term sums the errors across many compute calls to allow for
      # external factors like wind speed and friction
      #---------------------------------------------------------------------------
      self.i_error += (error + self.last_error) * dt
      i_error = self.i_error

      #---------------------------------------------------------------------------
      # The differential term accounts for the fact that as error approaches 0,
      # the output needs to be reduced proportionally to ensure factors such as
      # momentum do not cause overshoot.
      #---------------------------------------------------------------------------
      d_error = (error - self.last_error) / dt
      
      #---------------------------------------------------------------------------
      # The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
      #---------------------------------------------------------------------------
      p_output = self.p_gain * p_error
      i_output = self.i_gain * i_error
      d_output = self.d_gain * d_error

      #---------------------------------------------------------------------------
      # Store off last input for the next differential calculation and time for next integral calculation
      #---------------------------------------------------------------------------
      self.last_error = error
      self.last_time = now

      #---------------------------------------------------------------------------
      # Return the output, which has been tuned to be the increment / decrement in ESC PWM
      #---------------------------------------------------------------------------
      print ("p= ", p_output, "i= ", i_output, "d= ", d_output)
      return p_output, i_output, d_output

#========================================================
class PID2:
    def __init__(self, p_gain, i_gain, d_gain, now):
      self.last_error = 0.0
      self.last_time = now
      self.p_gain = p_gain
      self.i_gain = i_gain
      self.d_gain = d_gain
      self.i_error = 0.0

    def Compute(self, input, target, now):
      dt = (now - self.last_time)
      error = target - input
      p_error = error
      self.i_error += (error + self.last_error) * dt
      i_error = self.i_error
      d_error = (error - self.last_error) / dt
      p_output = self.p_gain * p_error
      i_output = self.i_gain * i_error
      d_output = self.d_gain * d_error
      self.last_error = error
      self.last_time = now
      print ("p= ", p_output, "i= ", i_output, "d= ", d_output)
      return p_output, i_output, d_output
    
#========================================================
class PID3:
    def __init__(self, p_gain, i_gain, d_gain, now):
      self.last_error = 0.0
      self.last_time = now
      self.p_gain = p_gain
      self.i_gain = i_gain
      self.d_gain = d_gain
      self.i_error = 0.0

    def Compute(self, input, target, now):
      dt = (now - self.last_time)
      error = target - input
      p_error = error
      self.i_error += (error + self.last_error) * dt
      i_error = self.i_error
      d_error = (error - self.last_error) / dt
      p_output = self.p_gain * p_error
      i_output = self.i_gain * i_error
      d_output = self.d_gain * d_error
      self.last_error = error
      self.last_time = now
      print ("p= ", p_output, "i= ", i_output, "d= ", d_output)
      return p_output, i_output, d_output

#=======================================================
temp1_pid = PID1(Zoe_CLI.P1, Zoe_CLI.I1, Zoe_CLI.D1, time.time())
temp2_pid = PID2(Zoe_CLI.P2, Zoe_CLI.I2, Zoe_CLI.D2, time.time())
temp3_pid = PID3(Zoe_CLI.P3, Zoe_CLI.I3, Zoe_CLI.D3, time.time())

#used when PID Gain settings changed
def init_PID():
    print ("INIT PID")
    temp1_pid = PID1(float(Zoe_CLI.P1), float(Zoe_CLI.I1), float(Zoe_CLI.D1), time.time())
    temp2_pid = PID2(float(Zoe_CLI.P2), float(Zoe_CLI.I2), float(Zoe_CLI.D2), time.time())
    temp3_pid = PID3(float(Zoe_CLI.P3), float(Zoe_CLI.I3), float(Zoe_CLI.D3), time.time())

#====================================================
# Event Loop
print ('Press q to Quit or ? for Help')    
while True:
    #Read keyboard input from 'Terminal' input
    Zoe_CLI.cmd()
    
    if Zoe_CLI.PID_GainChangeFlag == True:
        init_PID()
        Zoe_CLI.PID_GainChangeFlag = False 
    
    # Read Tempeatures
    Zoe_Sensors.read_temperature1()
    Zoe_Sensors.read_temperature2()
    Zoe_Sensors.read_temperature3()
    
    # Read Shaft encoder
    Zoe_Sensors.encoder()
    
    #read Emergancy Shut down Push Button
    Zoe_Sensors.read_es_pb()
    
    #================================
    # Process PID 1
    if Zoe_CLI.PID1_run_state == True: 
        Zoe_CLI.heater1_state = False                       #Turn heater off
        Zoe_Outputs.heater1(Zoe_CLI.heater1_state)
        
        [p_out, i_out, d_out] = temp1_pid.Compute(Zoe_Sensors.new_temp1, int(Zoe_CLI.target1), time.time())
        power1 = p_out + i_out + d_out                      # PID OUT
        
        if power1 >= Threshold1:
            Zoe_CLI.heater1_state = True                    # Turn Heater on
    else:
        power1 = 0
        
    #================================
    # Process PID 2
    if Zoe_CLI.PID2_run_state == True: 
        Zoe_CLI.heater2_state = False 
        Zoe_Outputs.heater2(Zoe_CLI.heater2_state)
        
        [p_out, i_out, d_out] = temp2_pid.Compute(Zoe_Sensors.new_temp2, int(Zoe_CLI.target2), time.time())
        power2 = p_out + i_out + d_out
        
        if power2 >= Threshold2:
            Zoe_CLI.heater2_state = True
    else:
        power2 = 0
        
    #================================
    # Process PID 3
    if Zoe_CLI.PID3_run_state == True: 
        Zoe_CLI.heater3_state = False
        Zoe_Outputs.heater3(Zoe_CLI.heater3_state)
        
        [p_out, i_out, d_out] = temp3_pid.Compute(Zoe_Sensors.new_temp3, int(Zoe_CLI.target3), time.time())
        power3 = p_out + i_out + d_out
        
        if power3 >= Threshold3:
            Zoe_CLI.heater3_state = True 
    else:
        power3 = 0
    
    #===============================
    # Over Temperature alarm if temp is > target + Offest
    offset = 80
    
    if Zoe_Sensors.new_temp1 >= (int(Zoe_CLI.target1) + offset) and (Zoe_ConfigFile.overtemp_alarm1 == False):
        Zoe_ConfigFile.overtemp_alarm1 = True
        Zoe_CLI.pizo_state = True
    
    if Zoe_Sensors.new_temp1 <= int(Zoe_CLI.target1) and (Zoe_ConfigFile.overtemp_alarm1 == True ):
        Zoe_ConfigFile.overtemp_alarm1 = False
        Zoe_CLI.pizo_state = False
    
    if Zoe_Sensors.new_temp2 >= (int(Zoe_CLI.target2) + offset) and (Zoe_ConfigFile.overtemp_alarm2 == False):
        Zoe_ConfigFile.overtemp_alarm2 = True
        Zoe_CLI.pizo_state = True
    
    if Zoe_Sensors.new_temp2 <= int(Zoe_CLI.target2) and (Zoe_ConfigFile.overtemp_alarm2 == True ):
        Zoe_ConfigFile.overtemp_alarm2 = False
        Zoe_CLI.pizo_state = False
    
    if Zoe_Sensors.new_temp3 >= (int(Zoe_CLI.target3) + offset) and (Zoe_ConfigFile.overtemp_alarm3 == False):
        Zoe_ConfigFile.overtemp_alarm3 = True
        Zoe_CLI.pizo_state = True
    
    if Zoe_Sensors.new_temp3 <= int(Zoe_CLI.target3) and (Zoe_ConfigFile.overtemp_alarm3 == True ):
        Zoe_ConfigFile.overtemp_alarm3 = False
        Zoe_CLI.pizo_state = False
        
    #===============================
    # Turn Outputs On/Off
    Zoe_Outputs.heater1(Zoe_CLI.heater1_state)
    Zoe_Outputs.heater2(Zoe_CLI.heater2_state)
    Zoe_Outputs.heater3(Zoe_CLI.heater3_state)
    
    Zoe_Outputs.alarm_pizo(Zoe_CLI.pizo_state)
 
    # Status display
    print ()
    print ("Name\t Heater\t PID Out\tCurrent\t Target\t Run\t  P\t I\t D\t ")
    print ("PID 1\t",
           Zoe_CLI.heater1_state, "\t",
           power1, "\t\t",
           Zoe_Sensors.new_temp1,"\t",
           Zoe_CLI.target1, "\t",
           Zoe_CLI.PID1_run_state,
           "\t", Zoe_CLI.P1, "\t",
           Zoe_CLI.I1, "\t",
           Zoe_CLI.D1)
    print ("PID 2\t",
           Zoe_CLI.heater2_state, "\t",
           power2, "\t\t",
           Zoe_Sensors.new_temp2,"\t",
           Zoe_CLI.target2, "\t",
           Zoe_CLI.PID2_run_state,
           "\t", Zoe_CLI.P2, "\t",
           Zoe_CLI.I2, "\t",
           Zoe_CLI.D2)
    print ("PID 3\t",
           Zoe_CLI.heater3_state, "\t",
           power3, "\t\t",
           Zoe_Sensors.new_temp3,"\t",
           Zoe_CLI.target3, "\t",
           Zoe_CLI.PID3_run_state,
           "\t", Zoe_CLI.P3, "\t",
           Zoe_CLI.I3, "\t",
           Zoe_CLI.D3)
    
#===================================================================================================
    
    sleep(3)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
    #process_variable = 20     # Initial temperature
    # Simulate the process
    #for t in plottime:
    # PID control output
    #control_output = pid.compute(process_variable, dt)
    #control_output= Zoe_Sensors.new_temp1    
    # Simulate process dynamics (heating rate proportional to control output)
    # process_variable += control_output * dt - 0.1 * (process_variable - 20) * dt  # Heat loss
    
    # Store the process variable
    # process_values.append(process_variable)    #this would be PID output
    process_values.append(str(Zoe_Sensors.new_temp1))
    #print ("PlotTemp")
    # Plot results
    setpoint = Zoe_CLI.target1
    plt.figure(figsize=(10, 6))
    plt.plot(str(time), process_values, label='Process Variable (Temperature)')
    plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature')
    plt.title('PID Controller Simulation')
    plt.legend()
    plt.grid()
    plt.show()
'''
         
