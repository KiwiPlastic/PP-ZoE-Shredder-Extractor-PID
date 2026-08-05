#!/usr/bin/python
import spidev
import max6675
from time import sleep
while True:
    sensor_0_0 = max6675.Max6675(0, 0)
    print (sensor_0_0.temperature)
    sleep(2)
