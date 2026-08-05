# ZoE: PID
import sys
from sys import stdout 			# This and the import below allow error signal reading to be displayed continuously on command line
import time
from time import sleep
from datetime import datetime

import Zoe_Sensors
import Zoe_Outputs
import Zoe_CLI
import Zoe_ConfigFile

target1 = Zoe_CLI.target1
P1 = Zoe_CLI.P1
I1 = Zoe_CLI.I1
D1 = Zoe_CLI.D1
interror1 = Zoe_ConfigFile.interror1
error1 = Zoe_ConfigFile.error1
power1 = Zoe_ConfigFile.power1
PID1_run_state = Zoe_CLI.PID1_run_state
heater1_state = Zoe_CLI.heater1_state

target2 = Zoe_CLI.target2
P2 = Zoe_CLI.P2
I2 = Zoe_CLI.I2
D2 = Zoe_CLI.D2
interror2 = Zoe_ConfigFile.interror2
error2 = Zoe_ConfigFile.error2
power2 = Zoe_ConfigFile.power2
PID2_run_state = Zoe_CLI.PID2_run_state
heater2_state = Zoe_CLI.heater2_state

target3 = Zoe_CLI.target3
P3 = Zoe_CLI.P3
I3 = Zoe_CLI.I3
D3 = Zoe_CLI.D3
interror3 = Zoe_ConfigFile.interror3 
error3 = Zoe_ConfigFile.error3
power3 = Zoe_ConfigFile.power3
PID3_run_state = Zoe_CLI.PID3_run_state
heater3_state = Zoe_CLI.heater3_state

pizo_state = Zoe_CLI.pizo_state

new_temp1 = Zoe_Sensors.new_temp1
new_temp2 = Zoe_Sensors.new_temp2
new_temp3 = Zoe_Sensors.new_temp3



class PID:

   def __init__(self, p_gain, i_gain, d_gain, now):
      self.last_error = 0.0
      self.last_time = now

      self.p_gain = p_gain
      self.i_gain = i_gain
      self.d_gain = d_gain

      self.i_error = 0.0


   def Compute(self, input, target, now):
      dt = (now - self.last_time)

      #---------------------------------------------------------------------------
      # Error is what the PID alogithm acts upon to derive the output
      #---------------------------------------------------------------------------
      error = target - input

      #---------------------------------------------------------------------------
      # The proportional term takes the distance between current input and target
      # and uses this proportially (based on Kp) to control the ESC pulse width
      #---------------------------------------------------------------------------
      p_error = error

      #---------------------------------------------------------------------------
      # The integral term sums the errors across many compute calls to allow for
      # external factors like wind speed and friction
      #---------------------------------------------------------------------------
      self.i_error += (error + self.last_error) * dt
      i_error = self.i_error

      #---------------------------------------------------------------------------
      # The differential term accounts for the fact that as error approaches 0,
      # the output needs to be reduced proportionally to ensure factors such as
      # momentum do not cause overshoot.
      #---------------------------------------------------------------------------
      d_error = (error - self.last_error) / dt
      
      #---------------------------------------------------------------------------
      # The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
      #---------------------------------------------------------------------------
      p_output = self.p_gain * p_error
      i_output = self.i_gain * i_error
      d_output = self.d_gain * d_error

      #---------------------------------------------------------------------------
      # Store off last input for the next differential calculation and time for next integral calculation
      #---------------------------------------------------------------------------
      self.last_error = error
      self.last_time = now

      #---------------------------------------------------------------------------
      # Return the output, which has been tuned to be the increment / decrement in ESC PWM
      #---------------------------------------------------------------------------
      print ("p= ", p_output, "i= ", i_output, "d= ", d_output)
      return p_output, i_output, d_output


def PID():
    print ("PID start")
    
    global target1
    global P1
    global I1
    global D1
    global interror1
    global error1
    global power1
    global PID1_run_state
    global heater1_state
    
    global target2
    global P2
    global I2
    global D2
    global interror2
    global error2
    global power2
    global PID2_run_state
    global heater2_state
    
    global target3
    global P3
    global I3
    global D3
    global interror3
    global error3
    global power3
    global PID3_run_state
    global heater3_state
    
    global pizo_state
    
    global new_temp1
    global new_temp2
    global new_temp3
    
    target1 = Zoe_CLI.target1
    P1 = Zoe_CLI.P1
    I1 = Zoe_CLI.I1
    D1 = Zoe_CLI.D1
    interror1 = Zoe_ConfigFile.interror1
    error1 = Zoe_ConfigFile.error1
    power1 = Zoe_ConfigFile.power1
    PID1_run_state = Zoe_CLI.PID1_run_state
    heater1_state = Zoe_CLI.heater1_state

    target2 = Zoe_CLI.target2
    P2 = Zoe_CLI.P2
    I2 = Zoe_CLI.I2
    D2 = Zoe_CLI.D2
    interror2 = Zoe_ConfigFile.interror2
    error2 = Zoe_ConfigFile.error2
    power2 = Zoe_ConfigFile.power2
    PID2_run_state = Zoe_CLI.PID2_run_state
    heater2_state = Zoe_CLI.heater2_state

    target3 = Zoe_CLI.target3
    P3 = Zoe_CLI.P3
    I3 = Zoe_CLI.I3
    D3 = Zoe_CLI.D3
    interror3 = Zoe_ConfigFile.interror3 
    error3 = Zoe_ConfigFile.error3
    power3 = Zoe_ConfigFile.power3
    PID3_run_state = Zoe_CLI.PID3_run_state
    heater3_state = Zoe_CLI.heater3_state

    pizo_state = Zoe_CLI.pizo_state

    new_temp1 = Zoe_Sensors.new_temp1
    new_temp2 = Zoe_Sensors.new_temp2
    new_temp3 = Zoe_Sensors.new_temp3

    #PID1
    if (PID1_run_state == True):
        
        errorsignal = new_temp1 				#.readADCSingleEnded(0, pga, sps) # Defines error signal as the input signal on channel (address?) 0 on the ADC
        
        stdout.write("\rTemp Sensor : %d " % errorsignal)
        stdout.flush()
        stdout.write("\n")
   
        [p_out, i_out, d_out] = temp.pid.Compute(errorsignal, TEMP_TARGET, time.time())
   
        temp_out = p_out + i_out + d_out			# PID OUT
        print("temp Out = ", temp_out)
        power1 = int(temp_out/10)*10			#convert to int
        print("power1 = ", power1)

        
        
        
        #error1 = target1 - new_temp1
        #interror1 = interror1 + error1
        #power1 = D1 + ((P1 * error1) + ((I1 * interror1)))
        '''
        #if power > than base PID values turn output ON.  else turn output OFF
        if (power1 > pwr_op_on  ):
            print ("PID1 power ON")
            print()
            power1_state=True
            #led_heater1.to_red(True)
            #HEATER1.on()
        else:
            print ("PID1 power OFF")
            print ()
            power1_state=False
            #led_heater1.to_red(False)
            #HEATER1.off()
           
        #led_pidop1.to_green(power1_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power1 > pwr_op_alm_limit):
            print ("PID1 ALARM")
            print ()
            PID1_run_state = False
            PID1_alarm_state=True
            #led_runpid1.to_green(False)
            #led_heater1.to_red(False)
            #HEATER1.off()
            #led_alarm1.to_red(True)
            #ALMBUZZER.on()
         '''
        
    #PID2
    if (PID2_run_state == True):
        error2 = target2 - new_temp2
        interror2 = interror2 + error2
        power2 = D2 + ((P2 * error2) + ((I2 * interror2)))
    
        #if power > than base PID values turn output ON.  else turn output OFF
        if (power2 > pwr_op_on  ):
            print ("PID power2 ON")
            print()
            power2_state=True
            #led_heater2.to_red(True)
            #HEATER2.on()
        else:
            print ("PID power2 OFF")
            print ()
            power2_state=False
            #led_heater2.to_red(False)
            #HEATER2.off()
           
        #led_pidop2.to_green(power2_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power2 > pwr_op_alm_limit):
            print ("PID2 ALARM")
            print ()
            PID2_run_state = False
            PID2_alarm_state=True
            #led_runpid2.to_green(False)
            #led_heater2.to_red(False)
            #HEATER2.off()
            #led_alarm2.to_red(True)
            #ALMBUZZER.on()

    #PID3
    if (PID3_run_state == True):
        error3 = target3 - new_temp3
        interror3 = interror3 + error3
        power3 = D3 + ((P3 * error3) + ((I3 * interror3)))
    
        #if power > than base PID values turn output ON.  else turn output OFF
        if (power3 > pwr_op_on  ):
            print ("PID power3 ON")
            print()
            power3_state=True
            #led_heater3.to_red(True)
            #HEATER3.on()
        else:
            print ("PID power3 OFF")
            print ()
            power3_state=False
            #led_heater3.to_red(False)
            #HEATER3.off()
           
        #led_pidop3.to_green(power3_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power3 > pwr_op_alm_limit):
            print ("PID3 ALARM")
            print ()
            PID3_run_state = False
            PID3_alarm_state=True
            #led_runpid3.to_green(False)
            #led_heater3.to_red(False)
            #HEATER3.off()
            #led_alarm3.to_red(True)
            #ALMBUZZER.on()
    '''
    #preheat logic
    if preheat1_state:                                                           #if pre heat button been activated =True
        if new_temp1 >= target1 - preheat_trig:              # and if temp >= target - minus pre heat value
            PID1_alarm_state=True
            led_heater1.to_red(False)
            HEATER1.off()
            led_alarm1.to_red(True)
            ALMBUZZER.on()
            if pidautorun:                              # if auto pid run set in config window = TRUE
                PID1_run_state = True         # turn PID on
                sleep(2.0)                                #wait n secs, while buzzer sounds
                r1=PID1_reset()                     #reset and start PID1 (turns buzzer off)

    if preheat2_state:                                                           #if pre heat button been activated =True
        if new_temp2 >= target2 - preheat_trig:              # and if temp >= target - minus pre heat value
            PID2_alarm_state=True
            led_heater2.to_red(False)
            HEATER2.off()
            led_alarm2.to_red(True)
            ALMBUZZER.on()
            if pidautorun:                              # if auto pid run set in config window = TRUE
                PID2_run_state = True         # turn PID on
                sleep(2.0)                                #wait n secs, while buzzer sounds
                r2=PID2_reset()                     #reset and start PID1 (turns buzzer off)

    if preheat3_state:                                                           #if pre heat button been activated =True
        if new_temp3 >= target3 - preheat_trig:              # and if temp >= target - minus pre heat value
            PID3_alarm_state=True
            led_heater3.to_red(False)
            HEATER3.off()
            led_alarm3.to_red(True)
            ALMBUZZER.on()
            if pidautorun:                              # if auto pid run set in config window = TRUE
                PID3_run_state = True         # turn PID on
                sleep(2.0)                                #wait n secs, while buzzer sounds
                r3=PID3_reset()                     #reset and start PID1 (turns buzzer off)
    '''

    '''    
    print ("=========== Entering PID control loop ============")
    print ()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(new_temp1, new_temp2, new_temp3))
    print ()
    print ("TARGET 1 TEMP =",target1)
    print ("P1 =",P1)
    print ("I1 =",I1)
    print ("D1 =",D1)

    print ("Error1 = target - temp =", error1)
    print ("Int Error1 = Int Error + Error =",interror1)
    print()
    
    print ("Output on if >", pwr_op_on, "  : Power1 Output =", power1)
    print()    
    print ("TARGET 2 TEMP =",target2)
    print ("P2 =",P2)
    print ("I2 =",I2)
    print ("D2 =",D2)

    print ("Error2 = target - temp =", error2)
    print ("Int Error2 = Int Error + Error =",interror2)
    print ()
    #print ("Output on if >", pwr_op_on, "  : Power2 Output =", power2)

    print ()
    print ("TARGET 3 TEMP =",target3)
    print ("P3 =",P3)
    print ("I3 =",I3)
    print ("D3 =",D3)
    
    print ("Error3 = target - temp =", error3)
    print ("Int Error3 = Int Error + Error =",interror3)
    print ()
    
    #print ("Output on if >", pwr_op_on, "  : Power3 Output =", power3)
    print ()
    print ("Temp1 = ", new_temp1, "   Temp2 = ", new_temp2, "   Temp3 = ", new_temp3)
    print ("===========================================")
'''
'''
    # Update our labels on GUI page. Does not mean graphs. May not need pid1GUI as power1 is global
    Temp1GUI.set(new_temp1)
    Temp2GUI.set(new_temp2)
    Temp3GUI.set(new_temp3)
    pid1GUI.set(round (power1,0))
    pid2GUI.set(round (power2,0))
    pid3GUI.set(round (power3,0))
        
    # Append timestamp to x-axis list
    timestamp = mdates.date2num(dt.datetime.now())
    xs.append(timestamp)

    # this is our data arrays
    # Append sensor data to lists for plotting
    temp1.append(new_temp1)
    temp2.append(new_temp2)
    temp3.append(new_temp3)
    pid1out.append(power1)
    pid2out.append(power2)
    pid3out.append(power3)
   
    # Limit lists to a set number of elements
    xs = xs[-max_elements:]
    temp1= temp1[-max_elements:]
    temp2 = temp2 [-max_elements:]
    temp3 = temp3 [-max_elements:]
    pid1out = pid1out[-max_elements:]
    pid2out = pid2out[-max_elements:]
    pid3out = pid3out[-max_elements:]

    #----------------------------- Graph 1 Temp1 & PID OP1 --------------------------------------------
    # Clear, format, and plot pid1out values first (behind)
    color = 'tab:blue'
    ax1.clear()
    ax1.set_ylabel('PID 1', color=color)
    #ax1.set_xlim(15,40)                 # fix auto scale and set Temperature scale, not working
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.plot(xs, pid1out, linewidth=2, color=color)
    
    
    # This fulls the plot in. down to zero, is quite nice. works with ax1.collections lines
    #ax1.fill_between(xs, temp1, 0, linewidth=2, color=color, alpha=0.3)
    #ax1.fill_between(xs, temp1, linewidth=2, color=color, alpha=0.3)
    
    # Clear, format, and plot temp1 values (in front)
    color = 'tab:red'
    ax2.clear()
    ax2.set_ylabel('Temperature 1 (C)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(xs, temp1, linewidth=2, color=color)
    
    #-------------------------------  Graph 2 Temp2 PID OP2 --------------------------------------------
    # Clear, format, and plot pid2out values first (behind)
    color = 'tab:blue'
    ax3.clear()
    ax3.set_ylabel('PID 2', color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.plot(xs, pid2out, linewidth=2, color=color)

    # Clear, format, and plot temp2 values (in front)
    color = 'tab:red'
    ax4.clear()
    ax4.set_ylabel('Temperature 2 (C)', color=color)
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.plot(xs, temp2, linewidth=2, color=color)
    
    #---------------------------------  Graph 3 Temp 3 PID OP3 ------------------------------------------
    # Clear, format, and plot pid3out values first (behind)
    color = 'tab:blue'
    ax5.clear()
    ax5.set_ylabel('PID 3', color=color)
    ax5.tick_params(axis='y', labelcolor=color)
    ax5.plot(xs, pid3out, linewidth=2, color=color)

    # Clear, format, and plot temp3 values (in front)
    color = 'tab:red'
    ax6.clear()
    ax6.set_ylabel('Temperature 3 (C)', color=color)
    ax6.tick_params(axis='y', labelcolor=color)
    ax6.plot(xs, temp3, linewidth=2, color=color)

    #-----------------------------------------------------------------------------------------
    # Format timestamps to be more readable
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()
  
    # Make sure plots stay visible or invisible as desired
    #ax1.collections[0].set_visible(temp_plot_visible)      # Do  if theres a fill under the line 
    ax1.get_lines()[0].set_visible(Power_plot_visible)
    ax2.get_lines()[0].set_visible(temp_plot_visible)
    ax3.get_lines()[0].set_visible(Power_plot_visible)
    ax4.get_lines()[0].set_visible(temp_plot_visible)
    ax5.get_lines()[0].set_visible(Power_plot_visible)
    ax6.get_lines()[0].set_visible(temp_plot_visible)
'''    
#==============================================================================

