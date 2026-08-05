# Zoe GUI code

#========================================
def config():						# Display config window used to edit base config values

    print ("at config")
        
    global update_interval           # Time (ms) between polling/animation updates
    global max_elements              # Maximum number of elements to store in plot lists
    global pwr_op_alm_limit          # Max value PID ouput will get to before alarm shut down ( Heater not working)
    global pwr_op_on                 # PID power base line must get above to turn on
    global pidautorun
    global preheat_trig
    global open_folder
    
    global entry_update_interval
    global entry_max_elements
    global entry_pwr_op_on
    global entry_pwr_op_alm_limit
    global entry_preheat_trig
    global entry_open_folder

    global configwin
    global intvar                               #this tracks the checkbox GUI status value sets pidautorun status
    
    configwin = tk.Toplevel(root)
    configwin.configure(bg='white')
    #configwin.geometry('950x900')              #let it self size, its a better result
    configwin.title("Configuration Window")

    intvar = tk.IntVar(configwin)                   # init veriable for check box

    label_con0 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con1 = tk.Label(configwin, text='Graph update Interval (ms) : ', font=dfont, bg='white')
    label_con2 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con3 = tk.Label(configwin, text='Max Elements in Graph : ', font=dfont, bg='white')
    label_con4 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con5 = tk.Label(configwin, text='PID output threshold : ', font=dfont, bg='white')
    label_con6 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con7 = tk.Label(configwin, text='Max PID output before Alarm : ', font=dfont, bg='white')
    label_con8 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con9= tk.Label(configwin, text='Auto PID_run : ', font=dfont, bg='white')
    label_con10 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con11= tk.Label(configwin, text='PID_run = Target Temp(c) - n,   n=: ', font=dfont, bg='white')
    label_con12 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con13 = tk.Label(configwin, text='Default Data Folder location : ', font=dfont, bg='white')
    label_con14  = tk.Label(configwin, text='     ' , font=dfont, bg='white')
    label_conB1 = tk.Label(configwin, text='    ', font=dfont, bg='white')
    label_conB2 = tk.Label(configwin, text='    ', font=dfont, bg='white')
     
    entry_update_interval = tk.Entry(configwin,  font=dfont, bg='white',  width=8)
    entry_update_interval.insert(0, update_interval)

    entry_max_elements = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_max_elements.insert(0, max_elements)

    entry_pwr_op_on = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_pwr_op_on.insert(0, pwr_op_on)

    entry_pwr_op_alm_limit = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_pwr_op_alm_limit.insert(0, pwr_op_alm_limit)

    entry_preheat_trig = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_preheat_trig.insert(0, preheat_trig)

    entry_open_folder = tk.Entry(configwin, font=dfont, bg='white',  width=30)
    entry_open_folder.insert(0, open_folder)
   
    intvar.set(pidautorun)
    print("Value of:  intvar.set(pidautorun)", intvar.get()) 
    checkbutton_pidautorun = tk.Checkbutton(configwin, variable=intvar, onvalue = 1, offvalue = 0, bg='white')

    button_save_close = tk.Button(    configwin, 
                            text="Save & Close", 
                            font=dfont,
                            command = configwin_save_close)
   
    label_conB1.grid(row=0, column=0, sticky=tk.W)                   # blank
    label_con0.grid(row=1, column=1, sticky=tk.E)                       # blank
    label_con1.grid(row=2, column=1, sticky=tk.E)                       # graph update interval
    label_con2.grid(row=3, column=1, sticky=tk.E)                       # blank
    label_con3.grid(row=4, column=1, sticky=tk.E)                       # max elements
    label_con4.grid(row=5, column=1, sticky=tk.E)                       # blank
    label_con5.grid(row=6, column=1, sticky=tk.E)                       #PID output treshold
    label_con6.grid(row=7, column=1, sticky=tk.E)                       # blank
    label_con7.grid(row=8, column=1, sticky=tk.E)                       # max pid out before alarm
    label_con8.grid(row=9, column=1, sticky=tk.E)                       # blank
    label_con9.grid(row=10, column=1, sticky=tk.E)                     # Auto PID run
    label_con10.grid(row=11, column=1, sticky=tk.E)                   # blank
    label_con11.grid(row=12, column=1, sticky=tk.E)                   #Prehaet PID run trigger (C)
    label_con12.grid(row=13, column=1, sticky=tk.E)                   # blank
    label_con13.grid(row=14, column=1, sticky=tk.E)                   # default folder location
    label_con14.grid(row=15, column=3, sticky=tk.E)                   # blank
    label_conB2.grid(row=16, column=3, sticky=tk.E)                   # blank
        
    entry_update_interval.grid(row=2, column=2, sticky=tk.W)
    entry_max_elements.grid(row=4, column=2, sticky=tk.W)
    entry_pwr_op_on.grid(row=6, column=2, sticky=tk.W)
    entry_pwr_op_alm_limit.grid(row=8, column=2, sticky=tk.W)
    checkbutton_pidautorun.grid(row=10, column=2, sticky=tk.W)
    entry_preheat_trig.grid(row=12, column=2, sticky=tk.W)
    entry_open_folder.grid(row=14, column=2, sticky=tk.E)

    button_save_close.grid(row = 15, column = 3)
    
    canvas.draw()

#-----------------------------------------------------------------------------------------
#===========================================
def configwin_save_close():				# Config Window, button  "Save Entry's & close window"

    print ('at configwin_save_close')

    global update_interval             # Time (ms) between polling/animation updates
    global max_elements                # Maximum number of elements to store in plot lists
    global pwr_op_on                   # PID power base line must get above to turn on
    global pwr_op_alm_limit            # Max value PID ouput will get to before alarm shut down ( Heater not working)
    global pidautorun
    global preheat_trig
    global open_folder
    
    global entry_update_interval
    global entry_max_elements
    global entry_pwr_op_on
    global entry_pwr_op_alm_limit
    global entry_preheat_trig
    global entry_open_folder
    
    global configwin
    global intvar
    
    # get target value and error chk
    try:
        value = int(entry_update_interval.get())
        print(value)
        if value != update_interval:             #!=,  is not, or not equal
            print("it does not equal")
            update_interval = value
            #msgbox updat interval changed save to Defaults.txt and restart
            #updateinterval()
    except ValueError:
        print ("Invalid Value in update_interval entry box")

    # get target value and error chk
    try:
        value = int(entry_max_elements.get())
        print(value)
        max_elements = value
    except ValueError:
        print("Invalid Value in max_elements entry box")
    
    # get target value and error chk
    try:
        value = int(entry_pwr_op_on.get())
        print(value)
        pwr_op_on = value
    except ValueError:
        print("Invalid Value in pwr_op_on entry box")

    # get target value and error chk
    try:
        value = int(entry_pwr_op_alm_limit.get())
        print(value)
        pwr_op_alm_limit = value
    except ValueError:
        print("Invalid Value in pwr_op_alm_limit entry box")

    # get target value and error chk
    try:
        value = (intvar.get())
        print(value)
        pidautorun = value
    except ValueError:
        print("Invalid entry in checkbutton box")

    # get target value and error chk
    try:
        value = int(entry_preheat_trig.get())
        print(value)
        preheat_trig = value
    except ValueError:
        print("Invalid Value in Preheat entry box")
        
    # get target value and error chk
    try:
        value = (entry_open_folder.get())
        print(value)
        open_folder = value
    except ValueError:
        print("Invalid Value in open folder entry box")

    pass
    configwin.destroy()
        
#=====================================
def help_window():					# Button: Help 

    print ('at help_window')

    helpwin = tk.Toplevel(root)
    helpwin.geometry('950x900')
    helpwin.title("Help Window")
    msg = tk.Message(helpwin, text=helptxt, font = 12, width = 950)
    msg.pack()
    
#========================================
def toggle_Power():					# Button: Toggle the PID Power plot

    print('at toggle_Power')
    
    global canvas
    global ax1
    global ax2
    global ax5
    global Power_plot_visible

    
    # Toggle plot and axis ticks/label
    Power_plot_visible = not Power_plot_visible
    ax1.get_lines()[0].set_visible(Power_plot_visible)
    ax1.get_yaxis().set_visible(Power_plot_visible)
    ax3.get_lines()[0].set_visible(Power_plot_visible)
    ax3.get_yaxis().set_visible(Power_plot_visible)
    ax5.get_lines()[0].set_visible(Power_plot_visible)
    ax5.get_yaxis().set_visible(Power_plot_visible)
    
    canvas.draw()

#========================================
def toggle_temp():					# Button: Toggle the temperature plot

    print('at toggle_temp')
    
    global canvas
    global ax2
    global ax4
    global ax6
    global temp_plot_visible

    
    # Toggle plot and axis ticks/label
    temp_plot_visible = not temp_plot_visible
    #ax1.collections[0].set_visible(temp_plot_visible)      #required if using a fill under the line
    ax2.get_lines()[0].set_visible(temp_plot_visible)
    ax2.get_yaxis().set_visible(temp_plot_visible)
    ax4.get_lines()[0].set_visible(temp_plot_visible)
    ax4.get_yaxis().set_visible(temp_plot_visible)
    ax6.get_lines()[0].set_visible(temp_plot_visible)
    ax6.get_yaxis().set_visible(temp_plot_visible)
  
    canvas.draw()

#============================================
def manual_ctrl():					# Button: Toggel manual ctrl
    
    print('at manual_ctrl')

    global manual_state
    global led_manual
    global PID1_run_state
    global led_runpid1
    global preheat1_state
    global PID2_run_state
    global led_runpid2
    global preheat2_state
    global PID3_run_state
    global led_runpid3
    global preheat3_state
    
    manual_state = not manual_state
    led_manual. to_red(manual_state)

    r1 = PID1_reset()
    PID1_run_state = False
    led_runpid1. to_green(PID1_run_state)

    r2 = PID2_reset()
    PID2_run_state = False
    led_runpid2. to_green(PID2_run_state)

    r3 = PID3_reset()
    PID3_run_state = False
    led_runpid3. to_green(PID3_run_state)
    
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel heater1
def heater1():
    
    print('at heater1')
    
    global heater1_state
    global led_heater1
    global manual_state
    global preheat1_state
    global PID1_run_state
    
    if (PID1_run_state == False):                               #pid IS oFF ....
        
        if (manual_state == True):                                  # manual is ON
            heater1_state = not heater1_state               # toggel heater ON/Off
                    
        else:                                       #preheat is turning on, manual = off, PID is off
            preheat1_state = not preheat1_state
            heater1_state = not heater1_state
            led_pidop1.to_green(False)
            led_alarm1.to_red(False)
            ALMBUZZER.off()
            
        if (heater1_state == True):
            HEATER1.on()
            led_heater1. to_red(heater1_state)
        else:                                       # turn off
            HEATER1.off()
            led_heater1. to_red(heater1_state)          #false = off
            r1=PID1_reset()
            
    print ('preheat1_state =', preheat1_state)

    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel heater2
def heater2():
    
    print('at heater2')
    
    global heater2_state
    global led_heater2
    global manual_state
    global preheat2_state
    global PID2_run_state
    
    if (PID2_run_state == False):
        
        if (manual_state == True):
            heater2_state = not heater2_state

        else:
            preheat2_state = not preheat2_state
            heater2_state = not heater2_state
            led_pidop2.to_green(False)
            led_alarm2.to_red(False)
            ALMBUZZER.off()
               
        if (heater2_state == True):
            HEATER2.on()
            led_heater2. to_red(heater2_state)
        else:
            HEATER2.off()
            led_heater2. to_red(heater2_state)
            r2=PID2_reset()
        
    print ('preheat2_state = ', preheat2_state)
           
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel heater3
def heater3():
    
    print('at heater3')
    
    global heater3_state
    global led_heater3
    global manual_state
    global preheat3_state
    global PID3_run_state
    
    if (PID3_run_state == False):
            
        if (manual_state == True):
            heater3_state = not heater3_state

        else:
            preheat3_state = not preheat3_state
            heater3_state = not heater3_state
            led_pidop3.to_green(False)
            led_alarm3.to_red(False)
            ALMBUZZER.off()
            
        if (heater3_state == True):
            HEATER3.on()
            led_heater3. to_red(heater3_state)
        else:
            HEATER3.off()
            led_heater3. to_red(heater3_state)
            r3=PID3_reset()
        
    print ('preheat3_state = ', preheat3_state)
    
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID1 Run
def PID1_run():
    
    print("at PID1_run")
    
    global PID1_run_state
    global manual_state
    global led_runpid1
    global PID1_alarm_state

    if (manual_state == False):                             # If manual OFF...then change PID run state
        if (PID1_alarm_state == True):                   # If PID alarm....
            ALMBUZZER.off()                                      # turn off buzzer
            PID1_alarm_state = (False)
        else:                                                                    # else change PID run state
            PID1_run_state = not PID1_run_state
            led_runpid1. to_green(PID1_run_state)
            led_pidop1.to_green(False)
            heater1_state = (False)
            led_heater1. to_red(heater1_state)
            HEATER1.off()

            if (PID1_run_state == True):                        # restart PID, so reset variables
                r1=PID1_reset()
        
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID2 Run
def PID2_run():
    
    print('at PID2_run')
    
    global PID2_run_state
    global manual_state
    global led_runpid2
    global PID2_alarm_state

    if (manual_state == False):                             # If manual OFF...then change PID run state
        if (PID2_alarm_state == True):                   # If PID alarm....
            ALMBUZZER.off()                                      # turn off buzzer
            PID2_alarm_state = (False)
        else:                                                                    # else change PID run state
            PID2_run_state = not PID2_run_state
            led_runpid2. to_green(PID2_run_state)
            led_pidop2.to_green(False)
            heater2_state = (False)
            led_heater2. to_red(heater2_state)
            HEATER2.off()

            if (PID2_run_state == True):                    # restart PID, so reset variables
                r2 = PID2_reset()
        
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID3 Run
def PID3_run():
    
    print('at PID3_run')
    
    global PID3_run_state
    global manual_state
    global led_runpid3
    global PID3_alarm_state

    if (manual_state == False):                             # If manual OFF...then change PID run state
        if (PID3_alarm_state == True):                   # If PID alarm....
            ALMBUZZER.off()                                      # turn off buzzer
            PID3_alarm_state = (False)
        else:                                                                    # else change PID run state
            PID3_run_state = not PID3_run_state
            led_runpid3. to_green(PID3_run_state)
            led_pidop3.to_green(False)
            heater3_state = (False)
            led_heater3. to_red(heater3_state)
            HEATER3.off()

            if (PID3_run_state == True):                    # restart PID, so reset variables
                r3 = PID3_reset()
        
    canvas.draw()
