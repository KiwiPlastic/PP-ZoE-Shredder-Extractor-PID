#ZoE: Shut Down - PID resest
#-----------------------------------------------------------------------------
# PID1 reset every thing to off, include PID calcs and output, called at verious points
def PID1_reset():
    
    print("at PID1_Reset")
    
    global PID1_run_state
    global heater1_state
    global error1
    global interror1
    global power1
    global PID1_alarm_state
    
    PID1_run_state = (False)
    heater1_state = (False)
    error1 = 0
    interror1 = 0
    power1 = 0
    PID1_alarm_state = (False)
    
    return(PID1_run_state, heater1_state, error1, interror1, power1, PID1_alarm_state)

#-----------------------------------------------------------------------------
# PID2 reset every thing to off, include PID calcs and output, called at verious points
def PID2_reset():
    
    print("at PID2_Reset")
    
    global PID2_run_state
    global power2_state
    global heater2_state
    global error2
    global interror2
    global power2
    global PID2_alarm_state
    global preheat2_state
    
    led_runpid2.to_green(PID2_run_state)
    power2_state = False
    led_pidop2.to_green(power2_state)
    error2 = 0
    interror2 = 0
    power2 = 0
    heater2_state = (False)
    led_heater2. to_red(heater2_state)
    HEATER2.off()
    led_alarm2.to_red(False)
    PID2_alarm_state = (False)
    preheat2_state = False
    ALMBUZZER.off()

#-------------------------------------------------------------------------------------
# PID3 reset every thing to off, include PID calcs and output, called at verious points
def PID3_reset():
    
    print("at PID3_Reset")
    
    global PID3_run_state
    global power3_state
    global heater3_state
    global error3
    global interror3
    global power3
    global PID3_alarm_state
    global preheat3_state
        
    led_runpid3.to_green(PID3_run_state)
    power3_state = False
    led_pidop3.to_green(power3_state)
    error3 = 0
    interror3 = 0
    power3 = 0
    heater3_state = (False)
    led_heater3. to_red(heater3_state)
    HEATER3.off()
    led_alarm3.to_red(False)
    PID3_alarm_state = (False)
    preheat3_state = False
    ALMBUZZER.off()
