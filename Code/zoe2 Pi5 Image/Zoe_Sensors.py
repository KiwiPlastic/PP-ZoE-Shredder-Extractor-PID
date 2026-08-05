# ZoE: Measures all sensor inputs

'''
# SPI1 GPIO pins, device 0,1,2 (3 devices)
# 16 CE2     - Temp3 CS
# 17 CE1     - Temp2 CS
# 18 CE0     - Temp1 CS
# 19 MISO
# 20 MOSI
# 21 SCLK

# to test SPI is configured, via Terminal

richn@PPZOE:~ $
ls -1 /dev/spidev*

#returns with something like this
#/dev/spidev0.0
#/dev/spidev0.1
#/dev/spidev1.0
#/dev/spidev1.1
#/dev/spidev1.2
#richn@PPZOE:~ $ 

# this would indicate SPI Bus 0 has 2 devices and Bus 1 has 3 devices
'''

from gpiozero import Button
import os
import spidev

spi = spidev.SpiDev()

OPTO1_PIN = 5     # Encoder Opto1 Interupter IP
OPTO2_PIN = 6     # Encoder Opto2 Interupt IP

ES_PB_PIN = 26

emergancy_shutdown_pb = Button (ES_PB_PIN)

opto1_pb = Button (OPTO1_PIN)
opto2_pb = Button (OPTO2_PIN)

new_temp1 = 0
new_temp2 = 0
new_temp3 = 0

#===========================================================
# SPI MAX6675 0- 1024 deg K type termocouple  
def read_temperature1(decimals = 1):
    global new_temp1
    try:
        # Open SPI bus 1, device 0
        spi.open(1, 0)                    
        spi.max_speed_hz = 50000          
        temp1_data = [0,0]
        temp1_data = spi.xfer2(temp1_data)
        new_temp1 = temp1_data[0] << 8 | temp1_data[1]
        new_temp1 = (new_temp1 >> 3) / 4.0
        #new_temp1 = round(float(temp_string) / 1000.0, decimals)    #example code how to use decimals
        spi.close()
        return (new_temp1)
    except Exception:
        print ("Temp 1 SPI Failled")
        pass
    
def read_temperature2(decimals = 1):
    global new_temp2
    try:
        # Open SPI bus 1, device 1
        spi.open(1, 1)  
        spi.max_speed_hz = 50000  
        temp1_data = [0,0]
        temp1_data = spi.xfer2(temp1_data)
        new_temp2 = temp1_data[0] << 8 | temp1_data[1]
        new_temp2 = (new_temp2 >> 3) / 4.0
        spi.close()
        return (new_temp2)
    except Exception:
        print ("Temp 2 SPI Failled")
        pass
    
def read_temperature3(decimals = 1):
    global new_temp3
    try:
        # Open SPI bus 1, device 2
        spi.open(1, 2)                         
        spi.max_speed_hz = 50000               
        temp1_data = [0,0]
        temp1_data = spi.xfer2(temp1_data)
        new_temp3 = temp1_data[0] << 8 | temp1_data[1]
        new_temp3 = (new_temp3 >> 3) / 4.0
        spi.close()
        return (new_temp3)
    except Exception:
        print ("Temp 3 SPI Failled")
        pass

#====================================================
def read_es_pb():
    global emergancy_stop
    try:
        emergancy_stop = False
        if emergancy_shutdown_pb.is_pressed:
            emergancy_stop = True
            print ("EMERGANCY STOP")        
            os.system("sudo shutdown -h now")
            return (emergancy_stop)
    except Exception:
        print ("ES Fail")
        pass
        
#====================================================
def encoder():
    print ("Rotary Encoder")
    try:
        if opto1_pb.is_active:
            print ("Opto 1 pressed")        
            #return ()
        else:
            print ("Opto 1 released")
            #return()
        if opto2_pb.is_active:
            print ("Opto 2 pressed")        
            #return ()
        else:
            print ("Opto 2 released")
        return()    
    
    except Exception:
        print ("Encoder Failed")
        pass
        