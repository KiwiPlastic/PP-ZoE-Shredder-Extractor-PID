# ZoE: Outputs

from gpiozero import LED

# SSR => Heat Band 1   OP
HEATER1_PIN = 22
HEATER2_PIN = 23
HEATER3_PIN = 24

# Mosfet => Alarm Pizo OP
ALMPIZO_PIN = 25


heater1op = LED(HEATER1_PIN)
heater2op = LED(HEATER2_PIN)
heater3op = LED(HEATER3_PIN)

pizeoalarm = LED(ALMPIZO_PIN)

#=========================================
def heater1(heater1_state):
    if heater1_state:
        heater1op.off()
    else:
        heater1op.on()
#=========================================
def heater2(heater2_state):
    if heater2_state:
        heater2op.off()
    else:
        heater2op.on()        

#=========================================
def heater3(heater3_state):
    if heater3_state:
        heater3op.off()
    else:
        heater3op.on()

#=========================================
def alarm_pizo(pizo_state):    
    if pizo_state:
        pizeoalarm.on()
    else:
        pizeoalarm.off()
 