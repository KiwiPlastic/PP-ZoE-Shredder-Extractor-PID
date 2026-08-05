#!/usr/bin/python
# coding: utf8

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time

import Adafruit_GPIO.SPI as SPI
#import MAX6675.MAX6675 as MAX6675
#import max6675 as MAX6675        				 # Serial temp sensor function, this seam to work
import max6675 as TempSensor 


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


#=====================================================================================
# Richards notes: what can be passed to this MAX6675 SPI Temperature function
#
# sensor = MAX6675.MAX66&5(CLK, CS, DO, SPI, GPIO)
# temp = sensor.readTempC()
# tempbuf = sensor.read16()

# CLK = 25 clock GPIO pin to be used 
# CS  = 24 Chip Select GPIO pin to be used
# DO  = 18 Data in from Thermocuple into GPIO pin to be used
# SPI = Not being used. selects hardware SPI see example. No Cs hardware does it, unles you Use GPIO pins an ctrl yourself
# GPIO = Not being used. selects GPIO pin numbers(default) or pcb
# 
# Software SPI gives better control on chip select, for more than two SPI devices
#=========================================================================================


# Uncomment one of the blocks of code below to configure your Pi to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.
CLK = 14
CS  = 2
DO  = 15
#sensor = MAX6675(CLK, CS, DO)
#sensor = MAX6675(CLK, DO)
sensor = TempSensor(CLK, CS, DO)

# Raspberry Pi hardware SPI configuration.
# SPI_PORT   = 0
# SPI_DEVICE = 0
# sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


# Loop printing measurements every second.
print ('Press Ctrl-C to quit.')
while True:
	temp = sensor.readTempC()
	print ('Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp)))
	time.sleep(1.0)
