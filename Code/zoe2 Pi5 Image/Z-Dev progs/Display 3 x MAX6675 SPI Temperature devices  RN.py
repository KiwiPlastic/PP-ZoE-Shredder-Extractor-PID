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
import MAX6675.MAX6675 as MAX6675


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


#=====================================================================================
# Richards notes:
# I have used this test program to develop what i need
# It is to read 3 x Thermocpule temperatures from 3 x MAX6675 chip which are
# on the SPI bus. The MAX6675 uses chip select lines to activate each chip.
#
#  MAX6675 SPI Temperature function, what can be passed to thisand read from it
#
# sensor = MAX6675.MAX66&5(CLK, CS, DO, SPI, GPIO)
# temp = sensor.readTempC()
# tempbuf = sensor.read16()
#
#PIN numbering is GPIO not Pcb Header
#
# CLK = 14 clock GPIO pin to be used 
# CS1  = 2 Chip Select GPIO pin to be used
# CS2 = 3
# CS3 = 4
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
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)


# Raspberry Pi hardware SPI configuration.
# SPI_PORT   = 0
# SPI_DEVICE = 0
# sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


# Loop printing measurements every second.
print ('Press Ctrl-C to quit.')
while True:
        
#-------Original Program for One SPI device, also converts to Farenhight
#	temp = sensor.readTempC()
#	print ('Thermocouple Temperature: {0:0.3F}°C / {1:0.3F}°F'.format(temp, c_to_f(temp)))
#	time.sleep(1.0)
#-------------------------

	temp1 = sensor1.readTempC()
	temp2 = sensor2.readTempC()
	temp3 = sensor3.readTempC()
	print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp1, temp2,temp3))
	time.sleep(1.0)
