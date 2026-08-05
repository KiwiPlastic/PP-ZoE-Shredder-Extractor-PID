# ZoE: Outputs

import RPi.GPIO as GPIO

HEATER1_PIN = 22			# SSR => Heat Band 1   OP
HEATER2_PIN = 23
HEATER3_PIN = 24

ALMPIZO_PIN = 25			# Mosfet => Alarm Pizo OP

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(HEATER1_PIN, GPIO.OUT)
GPIO.setup(HEATER2_PIN, GPIO.OUT)
GPIO.setup(HEATER3_PIN, GPIO.OUT)

GPIO.setup(ALMPIZO_PIN, GPIO.OUT)

GPIO.output(HEATER1_PIN, GPIO.HIGH)
GPIO.output(HEATER2_PIN, GPIO.HIGH)
GPIO.output(HEATER3_PIN, GPIO.HIGH)

GPIO.output(ALMPIZO_PIN, GPIO.LOW)

#=========================================
def heater1(heater1_state):
    if heater1_state:
        GPIO.output(HEATER1_PIN, GPIO.LOW)
        #heater1_state = 0
        #print ("heater1_state = 1")
    else:
        GPIO.output(HEATER1_PIN, GPIO.HIGH)
        #heater1_state = 1
        #print ("heater1_state = 0")
        
#=========================================
def heater2(heater2_state):
    if heater2_state:
        GPIO.output(HEATER2_PIN, GPIO.LOW)
        #heater2_state = 0
        #print ("heater2_state = 1")
    else:
        GPIO.output(HEATER2_PIN, GPIO.HIGH)
        #heater2_state = 1
        #print ("heater2_state = 0")
        
#=========================================
def heater3(heater3_state):
    if heater3_state:
        GPIO.output(HEATER3_PIN, GPIO.LOW)
        #heater3_state = 0
        #print ("heater3_state = 1")
    else:
        GPIO.output(HEATER3_PIN, GPIO.HIGH)
        #heater3_state = 1
        #print ("heater3_state = 0")

#=========================================
def alarm_pizo(pizo_state):    
    if pizo_state:
        GPIO.output(ALMPIZO_PIN, GPIO.HIGH)		#off
        #print ("pizo_state = 1")
        #pizo_state = 0
    else:
        GPIO.output(ALMPIZO_PIN, GPIO.LOW)		#on
        #print ("pizo_state = 0")
        #pizo_state = 1
