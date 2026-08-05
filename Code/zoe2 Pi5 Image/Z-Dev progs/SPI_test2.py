#!/usr/bin/python3

# This is hardware SPI1 add following line to /boot/config.txt to enable SPI1 (3 chip selects)

#	dtoverlay=spi1-3cs					
#
# GPIO pins, device 0,1,2 (3 devices)
# 16 CE2
# 17 CE1
# 18 CE0
# 19 MISO
# 20 MOSI
# 21 SCLK



# test SPI is configured, via this CML
#richn@PPZOE:~ $ ls -1 /dev/spidev*
#/dev/spidev0.0
#/dev/spidev0.1
#/dev/spidev1.0
#/dev/spidev1.1
#/dev/spidev1.2
#richn@PPZOE:~ $ 

# would indicate all Hardware  SPI ports and channels are on

#/sys/bus/spi/devices/spi1.1

#spi.open_path(spidev_devicefile_path)
#to_send = [0x01, 0x02, 0x03]
#spi.xfer(to_send)

#spi.open_path("/dev/spidev0.0")


#========================================
from time import sleep

import spidev
spi = spidev.SpiDev()

while True:

    spi.open_path("/dev/spidev1.0")
    temp1_data = [0,0]
    temp1_data = spi.xfer2(temp1_data)
    print ("Temp1 : ", temp1_data[0], "    Temp1 : ", temp1_data[1])
    wdata = temp1_data[0] << 8 | temp1_data[1]
    wdata = (wdata>>3)/4.0
    #print (wdata)
    spi.close()

    spi.open_path("/dev/spidev1.1")
    temp2_data = [0,0]
    temp2_data = spi.xfer2(temp2_data)
    print ("Temp2 : ", temp2_data[0], "    Temp2 : ", temp2_data[1])
    spi.close()
    
    
    spi.open_path("/dev/spidev1.2")
    temp3_data = [0,0]
    temp3_data = spi.xfer2(temp3_data)
    print ("Temp3 : ", temp3_data[0], "    Temp3 : ", temp3_data[1])
    spi.close()
    print()
    sleep(2)



