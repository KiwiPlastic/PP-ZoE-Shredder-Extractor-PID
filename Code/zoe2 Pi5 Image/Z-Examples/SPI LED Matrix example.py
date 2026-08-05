#import modules
import spidev
import time

#initialise SPIDev
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 125000
time.sleep(0.0005)

#create our list to send on the SPI bus
to_send = []

#initialise variables
colour = 0x01
delay = 0.05

#set all LEDs to off
for i in range (0, 64):
    to_send.append(0x00)
    spi.xfer(to_send)

time.sleep(0.0005)  #delay for stability

#main loop
try:
    while 1:
        
        #if to_send list contains less than 64 values, add another byte to the list
        if to_send.count(colour) < 64:
            del to_send[:]
            for i in range(0,64):
                to_send.append(colour)
                spi.xfer(to_send)
                time.sleep(delay)
                
        #if the list is full (64 items), reset the list and replace each value with 0x00
        if to_send.count(colour) == 64:
            del to_send[:]
            for i in range(0, 64):
                to_send.append(0x00)
                spi.xfer(to_send)
                time.sleep(delay)
                
        colour = colour + 0x01  #cycle through the available colours

        if colour == 0x04:  #when the last colour is reached, reset to 0x01
            colour = 0x01
        
except KeyboardInterrupt:   #if Ctrl + C is pressed, cleanly exit our program
    for i in range (0, 64):
        to_send.append(0x00)
    spi.xfer(to_send)   
    spi.close()
    print("Program Exited")