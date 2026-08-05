#!/usr/bin/python3

# This is hardware SPI
# add following line to /boot/config.txt to enable
# 	dtoverlay=maxtherm,spi0-1,max6675
# 	or
#	dtoverlay=spi1-3cs
#
# SPI0 GPIO pins, device 0 (CE0) and device 1 (CE1)
# 7 CE1
# 8 CE0
# 9 MISO
# 10 MOSI
# 11 SCLK
#
# SPI1 GPIO pins, device 0,1,2 (3 devices)
# 16 CE2
# 17 CE1
# 18 CE0
# 19 MISO
# 20 MOSI
# 21 SCLK

# max6675 spi0-1
# /sys/bus/iio/devices/iio:device1/in_temp_scale
# /sys/bus/iio/devices/iio:device1/in_temp_raw

from time import sleep
while True:

    with open('/sys/bus/iio/devices/iio:device0/in_temp_scale', 'r') as dev1scale:
                scale1 = float(dev1scale.read())

    with open('/sys/bus/iio/devices/iio:device0/in_temp_raw', 'r') as dev1raw:
                raw1 = float(dev1raw.read())
                dev1temp = (scale1 * raw1) / 1000.0

    print ("Max6675: ", dev1temp)
    sleep(2)



