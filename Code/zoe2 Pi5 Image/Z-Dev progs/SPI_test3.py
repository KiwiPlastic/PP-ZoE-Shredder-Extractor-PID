#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import spidev
import time
import RPi.GPIO as GPIO


#unicode  python 2.7  VS 3.2  
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x



class Max6675:

  VALID_DATA   = 0 
  ERROR_CHANNEL = 1
  ERROR_PROBE   = 2
  ERROR_DATA    = 3

  errorString  = [ 'Temperature is Valid' , 'Multiplex channel 74HC138/139 error' ,
                        'Probe is not connected' , 'Max6675 returned bad data']


  def __init__(self,spiPort=0, spiDevice=0,HC138A = None , HC138B = None, HC138C = None):

    self.spi = spidev.SpiDev()
    self.spi.open(spiPort,spiDevice)
    self.HC138A = HC138A
    self.HC138B = HC138B
    self.HC138C = HC138C
    self.HC138Valid = False
    
    if (self.HC138A != None) or (self.HC138B != None) or (self.HC138C != None):
       self.HC138Valid = True
       GPIO.setwarnings(False)
       GPIO.setmode(GPIO.BCM)
         

    if self.HC138A != None:
       GPIO.setup(self.HC138A,GPIO.OUT)

    if self.HC138A != None:
       GPIO.setup(self.HC138B,GPIO.OUT)

    if self.HC138A != None:
       GPIO.setup(self.HC138C,GPIO.OUT)

    


  ''' get(Channel)
    if Channel as to be None if no 74HC138 is used
    otherwisw Channel specify the Y0 output which the Max6675 is connected

    Return

    The return is [ temperature  , ErrorCode]

    Where ErrorCode is

    0 : Data is valid
    1 : Bad Channel (is the 74HC138 GPIO set ?)
    2 : Probe unconnected
    3 : Max6675 return bad data

  '''

  def get(self,Channel=None):
    # Deal with 74HC138/139 Multiplexer if we have one
    if ((Channel == None) and  (self.HC138Valid)) or ((Channel != None) and (not self.HC138Valid)):
       return [None , self.ERROR_CHANNEL]

    if Channel != None:
      if Channel > 7 :
         return [None , self.ERROR_CHANNEL]
      if self.HC138A!=None:
       GPIO.output(self.HC138A, Channel & 1)
      if self.HC138B!=None:
       GPIO.output(self.HC138B, Channel & 2)
      if self.HC138C!=None:
       GPIO.output(self.HC138C, Channel & 4)

    #Now let's read the sensor

    data= [0,0]
    data = self.spi.xfer2(data)
    
    #Is the sensor data Valid
    if (data[1] & 2) == 2:
      return [ None , self.ERROR_DATA ]

    #Is the Probe connected
    if (data[1] & 4) == 4:
      return [ None , self.ERROR_PROBE ]    
            
    wdata = data[0] << 8 | data[1]
    return [(wdata>>3)/4.0  , self.VALID_DATA]



if __name__ == "__main__":


   max6675 = Max6675(0,0,17,27,22)

  
   for Probe in range(8):

     probeOK=False
     temperature=0

     data = max6675.get(Probe)


     #let's check if the data is Valid
     if data[1] != max6675.VALID_DATA:
       print('Probe {}: {}'.format(Probe,max6675.errorString[data[1]]))
     else:
       print('Probe {}: Temperature : {:.1f}'.format(Probe,data[0])+u('\u2103'))
