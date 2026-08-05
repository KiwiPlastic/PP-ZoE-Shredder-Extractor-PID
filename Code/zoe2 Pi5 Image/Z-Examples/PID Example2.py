import sys
from sys import stdout 			# This and the import below allow error signal reading to be displayed continuously on command line
import time
from time import sleep
from datetime import datetime

import RPi.GPIO as GPIO 		# Import the Pi's GPIO library
#import RPIO.PWM as PWM 		# Import the Pi's PWM library

GPIO.setmode(GPIO.BCM) 			# Set GPIO numbering system using GPIO numbers and not pin numbers

sys.path.insert(0, '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15') # Sets the import path to the appropriate folder containing ADC modules
                                #from Adafruit_ADS1x15 import ADS1x15 # Imports the appropriate ADC module
# Constants
pga = 6144 						# input('\nChoose 0256, 0512, 1024, 2048, 4096, or 6144 as the desired gain: ') # User enters desired gain
sps = 32 						# input('\nChoose  8, 16, 32, 64, 128, 250, 475, or 860 as the samples taken per second: ') # User enters desired sampling rate
new_temp = 1					# ADS1x15(ic=0x00) # Defines 'adc' variable; 'ic=0x00' denotes usage of the ADS1015, change to 'ic=0x01' for ADS1115

PID_TEMP_P_GAIN = 0.75
PID_TEMP_I_GAIN= 0.01
PID_TEMP_D_GAIN = 0.001

GPIO_BCM_PIN = 27				# HW PWM Out(servo)
CHANNEL = 1

TEMP_TARGET = 1000000

SUBCYCLE = 1000000 				# Sets servo subcycle to be 1 second (1 million microseconds)
GRANULARITY = 10
min_duty_cycle = 0
max_duty_cycle = 999990

#PWM Initialization
#servo.set_servo(GPIO_BCM_PIN, 0)	# ???PWM.Servo(CHANNEL, SUBCYCLE, GRANULARITY)
servo = 2 						


class PID:

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



GPIO.setup(GPIO_BCM_PIN, GPIO.IN)
state = GPIO.input(GPIO_BCM_PIN)			#Read PWM output pin?

temp_pid = PID(PID_TEMP_P_GAIN, PID_TEMP_I_GAIN, PID_TEMP_D_GAIN, time.time())


while True:
   # servo.stop_servo(GPIO_BCM_PIN)		# stop servo
   
   # Temp sensor reading
   errorsignal = new_temp 				#.readADCSingleEnded(0, pga, sps) # Defines error signal as the input signal on channel (address?) 0 on the ADC

   stdout.write("\rTemp Sensor : %d " % errorsignal)
   stdout.flush()
   stdout.write("\n")
   
   [p_out, i_out, d_out] = temp_pid.Compute(errorsignal, TEMP_TARGET, time.time())
   
   temp_out = p_out + i_out + d_out			# PID OUT
   print("temp Out = ", temp_out)
   duty_cycle = int(temp_out/10)*10			#convert to int
   print("duty = ", duty_cycle)

   if duty_cycle < min_duty_cycle:
      duty_cycle = min_duty_cycle
   if duty_cycle > max_duty_cycle:
      duty_cycle = max_duty_cycle

   if state ==  False: 									# read PWM output, if low...set value
      #servo.set_servo(GPIO_BCM_PIN, duty_cycle)		# his is the Pwm output
      servo=9 											#dummy line
   
   stdout.write("\r")
   sleep(2)   
