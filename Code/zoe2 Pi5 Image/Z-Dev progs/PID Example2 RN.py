# 18/8/20 RN
# this is first play with PID code
# this works with output to Shell, no input controls (that i can work)
# was originaly for PWM output
# example only

import os
from subprocess import Popen, PIPE, call
from optparse import OptionParser
from time import sleep

def tempdata():
    # Replace 28-000003ae0350 with the address of your DS18B20
    pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/28-000003ea0350/w1_slave"], stdout=PIPE)
    result = pipe.communicate()[0]
    # result_list = 30.2 #result.split()[0] #("=")
    # temp_mC = int(result_list[-1]) # temp in milliCelcius
    temp_mC = 56
    return temp_mC

def setup_1wire():
  os.system("sudo modprobe w1-gpio && sudo modprobe w1-therm")

def turn_on():
  os.system("sudo ./strogonanoff_sender.py --channel 4 --button 1 --gpio 0 on")

def turn_off():
  os.system("sudo ./strogonanoff_sender.py --channel 4 --button 1 --gpio 0 off") 

#Get command line options
parser = OptionParser()
parser.add_option("-t", "--target", type = int, default = 55)
parser.add_option("-p", "--prop", type = int, default = 6)
parser.add_option("-i", "--integral", type = int, default = 2)
parser.add_option("-b", "--bias", type = int, default = 22)
(options, args) = parser.parse_args()
target = options.target
print ('Target temp is %d' % (options.target))
P = options.prop
I = options.integral
D = options.bias
# Initialise some variables for the control loop
interror = 0
pwr_cnt=1
pwr_tot=0

# Setup 1Wire for DS18B20
setup_1wire()

# Turn on for initial ramp up
state="on"
turn_on()

temperature=tempdata()
print("Initial temperature ramp up")
while (target - temperature > 6000):
    sleep(2)
    temperature=tempdata()
    print(temperature, target)

print("Entering control loop")
while True:
    temperature=tempdata()
    error = target - temperature
    interror = interror + error
    #power = D + ((P * error) + ((I * interror)/100))/100
    power = D + ((P * error) + ((I * interror)))

    print("Temperature =",temperature)
    print("Target Temp =",target)
    print ("Error=target-temp =", error)
    print ("Int Error = Int error + Error",interror)
    print ("P =",P)
    print ("I =",I)
    print ("D =",D)
    print ("Power Output =", power)

    # Make sure that if power should be off then it is
    if (state=="off"):
        turn_off()
        print ("Pwr saftey set to Off")
    #if power > than base PID values turn output ON.  else turn output OFF
    if (power>22):
        print ("PID power ON")
        state="on"
        turn_on()
    else:
        print ("PID power OFF")
        state="off"
        turn_off()

    sleep(1)
    print ("state=", state)
    print ("=============================")
        
# Long duration pulse width modulation
#    for x in range (1, 25):
#        print (x)
#        if (power > x):
#            print ("got here")
#            if (state=="off"):
#                state="on"
#                print("On")
#                turn_on()
#        else:
##            print ("got here two")
#            if (state=="on"):
#                state="off"
#                print("Off")
#                turn_off()

