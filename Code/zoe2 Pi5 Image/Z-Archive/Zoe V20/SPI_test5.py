#!/usr/bin/python3
'''
#This is hardware SPI on RPI5 (works)

add following line to /boot/firmware/config.txt to enable SPI1 (3 chip selects)

dtoverlay=spi1-3cs

sudo nano config.txt

# GPIO pins, device 0,1,2 (3 devices)
# 16 CE2
# 17 CE1
# 18 CE0
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

# would indicate all Hardware  SPI ports and channels are on

optional format for below
#spi.open_path(spidev_devicefile_path)
#spi.open_path("/dev/spidev1.0")

'''


from time import sleep
import spidev

spi = spidev.SpiDev()

while True:
    spi.open(1, 0)  # Open SPI bus 1, device 0
    spi.max_speed_hz = 50000  # Set speed
    temp1_data = [0,0]
    temp1_data = spi.xfer2(temp1_data)
    #print ("Temp1 : ", temp1_data[0], "    Temp1 : ", temp1_data[1])
    deg1 = temp1_data[0] << 8 | temp1_data[1]
    deg1 = (deg1>>3)/4.0
    print (" Probe 1:", deg1)
    spi.close()

    spi.open(1, 1)  # Open SPI bus 1, device 0
    spi.max_speed_hz = 50000  # Set speed
    temp1_data = [0,0]
    temp1_data = spi.xfer2(temp1_data)
    #print ("Temp1 : ", temp1_data[0], "    Temp1 : ", temp1_data[1])
    deg2 = temp1_data[0] << 8 | temp1_data[1]
    deg2 = (deg2>>3)/4.0
    print (" Probe 2:", deg2)
    spi.close()

    spi.open(1, 2)  # Open SPI bus 1, device 0
    spi.max_speed_hz = 50000  # Set speed
    temp1_data = [0,0]
    temp1_data = spi.xfer2(temp1_data)
    #print ("Temp1 : ", temp1_data[0], "    Temp1 : ", temp1_data[1])
    deg3 = temp1_data[0] << 8 | temp1_data[1]
    deg3 = (deg3>>3)/4.0
    print (" Probe 3:", deg3)
    print()
    spi.close()
    sleep(2)
