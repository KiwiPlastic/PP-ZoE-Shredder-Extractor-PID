from gpiozero import LED
from time import sleep

led1 = LED(27)
led2 = LED(22)
led3 = LED(23)

while True:
    led1.on()
    sleep(1)
    led1.off()
    sleep(1)

    led2.on()
    sleep(1)
    led2.off()
    sleep(1)

    led3.on()
    sleep(1)
    led3.off()
    sleep(1)
    
