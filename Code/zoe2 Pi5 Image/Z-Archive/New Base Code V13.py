# NOTE edting the green text will effect the help display
helptxt = """
15-9-2020,  V12

This project is designed for a Precious Plastic Extruder or Injection machine.

It uses 3 thermocouples, to measure temperature, via 3 x MAX6675 SPI chips (Adreno accesory kitset).
Three GPIO pins connected to Solid State Relays (SSR-40 DA) to control Heat bands.

It incorporates 3 x PID contronlers, with a graphical live display of temperature and PID power output.

Each PID has a Run button, Target temperature, PID variables, Output on/off indicator, and Alarm output buzzer.

The alarm buzzer will sound if the PID power output gets to high, ie heater not working.
It then turns associated PID off. 

It can be put into Manual control, allowing the Heater outputs to be turned on/off individualy.

It also reads and writes configuration data to disk file.
Allowing different profile settings for defferent plastics, to be saved for later use.

HARDWARE:
Raspbery Pi ver 3B+ or ver 4B+
3 x MAX6675 SPI thermocouple interface PCB with thermocouple probes. Adreno accesory kitset.
3 x GPIO pins (heater output). These are connected directly to SSR-40 DA solid state relays. 3 volt input.
1 x Pizo Buzzer
1 x 7" touch screen (optional but recomended)

Sofware
    <ESC>   End GUI
    <F11>   Toggel full screen
    <ENTER>  To load values in entry fields
    
Writen in Python 3.5 on Raspbery Pi. Code will not work on Python 2 without changes.

Some libaries are required from Github. From folder wher they have been unzipped, use "sudo PIP3 name" to install them
    matplotlib           Provides animated graphs
    tk_tools               Provides LED indicators
    adafruit_GPIO     Provides chip selselect fuction for SPI chips
    MAX6675           Provides function to read SPI chips

If using a 7" touch screen it is recommend to install a vertual keyboard
https://pimylifeup.com/raspberry-pi-on-screen-keyboard/

Original code Source - this is a very helpfull link.
https://www.digikey.co.uk/en/maker/projects/python-gui-guide-introduction-to-tkinter/d04a764c78114682aac9255056026338

"""

# Dev history :
# Get 3 x graphs up -DONE V4
# Tidy up graphs. Max, Min ylim - wont work, fix later
# Add PID data to graphs - DONE V5
# Add PID code x 3 - Done V5
# Add notes - Done V6
# Add GPIO heaters and alarm buzzer - DONE V6 init only, not fully implimented
# GUI Interface setup - DONE V7
# GUI leds added - DONE V7
# GUI input fild fonts - done V7
# GUI blank the spacer label - done V7
# GUI row 13 buttons spacing - done V7
# GUI correct labels - done V7
# <ESC> = quit key, working - done V8
# functions to make heater/manual buttons work for GUI Leds and GPIO - done V8
# link entry values to PID variables, with error handling and updates on <Enter> key callback  - V9
# updated Shell print output of PID values - V9
# Heater GPIO pins off on exit via mouse quite or <ESC> pressed - V10
# Init and decalre all variables - V10
# link maual override - V10
# set up 3 x reset on PID Run buttons - V10
# link PID OP to heaters - V10
# minor plot toggel issue - V10
# alarm & buzzer function - V11
# write file to disk - V11
# help window (toplevel) - V11
# save, load & config buttons,  callback set up - V11
# GUI line between PIDs - V12
# config window - V12

#To Do
# Load variables from disk and Save to disk
# Load/Save dif Profiles
# Full testing - posible bug on PID run buttons

import tkinter as tk                                                  # GUI function
import tkinter.font as tkFont

import tk_tools                                                         # provids leds, and other GUI display elements

import matplotlib.figure as figure                       # Animated graphs
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Adafruit_GPIO.SPI as SPI                         # Serial temperature sensors Chip select
import MAX6675.MAX6675 as MAX6675        # Serial temp sensor function 

from gpiozero import LED                                      #GPIO pins and functions

from time import strftime                                       # used to write data to disk
import datetime as dt

#--------------------------------------------------------------------------------------------------------
# Config GPIO H/W pin asignment, using GPIO labeling, not pin header. Change these to realocate pins
HEATER1 = LED(22)
HEATER2 = LED(23)
HEATER3 = LED(27)
ALMBUZZER = LED(25)

CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15

# SPI MAX6675 software configuration (temperature Sensors)
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

#====================================================
#               INIT Global VARIABLES 
#====================================================

# Parameters
update_interval = 3000      # Time (ms) between polling/animation updates(read temps and update PID)
max_elements = 1440        # Maximum number of elements to store in plot lists
pwr_op_on = 10                    # PID power base line must get above to turn on
pwr_op_alm_limit = 100     # Max value PID ouput will get to before alarm shut down ( Heater not working)

# Initialise PID variables 
target1 = 27.1
P1 = 1
I1 = 1
D1= 0
interror1 = 0
error1 = 0
power1 = 0

target2 = 27.2
P2 = 1
I2 = 1
D2 = 0
interror2 = 0
error2 = 0
power2 = 0

target3 = 27.3
P3 = 1
I3 = 1
D3 = 0
interror3 = 0
error3 = 0
power3 = 0

# Declare global variables
root = None         #Parent
dfont = None       #Display Font size, used in resize of window
frame = None      #
canvas = None   #
ax1 = None          # Axis PID1_Out
ax2 = None          # Axis Temperature 1
ax3 = None          #Axis PID2_Out
ax4 = None          #Axis Temperature 2
ax5 = None          #Axis PID3_Out
ax6 = None          #Axis Temperature 3
temp_plot_visible = None
Power_plot_visible = None
PID1_run_state = None
PID2_run_state = None
PID3_run_state = None
manual_state = None
heater1_state = None
heater2_state = None
heater3_state = None
PID1_alarm_state = None
PID2_alarm_state = None
PID3_alarm_state = None

# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
Power_plot_visible = True
PID1_run_state = False
PID2_run_state = False
PID3_run_state = False
manual_state = False
heater1_state = False
heater2_state = False
heater3_state = False
PID1_alarm_state = False
PID2_alarm_state = False
PID3_alarm_state = False



###############################################################################
# Functions


#-----------------------------------------------------------------------------------------
# Button: Save as... Data to disk. This is under development to Read and Write profiles
def save_file():

    print ("at save file")
        # Update data to display temperature
    try:
        temp1= sensor1.readTempC()     #read SPI temp value
        temp2 = sensor2.readTempC()     #read SPI temp value
        temp3 = sensor3.readTempC()     #read SPI temp value
    except: 
        pass

    with open("/home/pi/Documents/Python/Zoe_temps.csv", "a") as log:
        log.write("{0},{1},{2},{3}\n".format(strftime("%d-%m-%y %H:%M:%S"),str(temp1),str(temp2),str(temp3)))


#-----------------------------------------------------------------------------------------
# Button: Load... Data from disk. This is under development to Read and Write profiles
def load_file():

    print ("at load file")
    
#-----------------------------------------------------------------------------------------
# Button: Config  window used to set base values
def config():

    print ("at config")
    global update_interval           # Time (ms) between polling/animation updates
    global max_elements             # Maximum number of elements to store in plot lists
    global pwr_op_alm_limit         # Max value PID ouput will get to before alarm shut down ( Heater not working)
    global pwr_op_on                    # PID power base line must get above to turn on
    global entry_update_interval
    global entry_max_elements
    global entry_pwr_op_on
    global entry_pwr_op_alm_limit
    global configwin
    
    configwin = tk.Toplevel(root)
    configwin.configure(bg='white')
    #configwin.geometry('950x900')
    configwin.title("Configuration Window")

    label_con0 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con1 = tk.Label(configwin, text='Graph update Interval,(Sensors & PID) : ', font=dfont, bg='white')
    label_con2 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con3 = tk.Label(configwin, text='Max Elements in Graph : ', font=dfont, bg='white')
    label_con4 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con5 = tk.Label(configwin, text='PID output threshold : ', font=dfont, bg='white')
    label_con6 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con7 = tk.Label(configwin, text='Max PID output before Alarm : ', font=dfont, bg='white')
    label_con8 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con9 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    label_con10 = tk.Label(configwin, text=' ', font=dfont, bg='white')
    
    entry_update_interval = tk.Entry(configwin, textvariable = sv, font=dfont, bg='white',  width=8)
    entry_update_interval.insert(0, update_interval)
    entry_update_interval.bind('<Key-Return>', on_update_interval_changed)

    entry_max_elements = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_max_elements.insert(0, max_elements)
    entry_max_elements.bind('<Key-Return>', on_max_elements_changed)

    entry_pwr_op_on = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_pwr_op_on.insert(0, pwr_op_on)
    entry_pwr_op_on.bind('<Key-Return>', on_pwr_op_on_changed)

    entry_pwr_op_alm_limit = tk.Entry(configwin, font=dfont, bg='white',  width=8)
    entry_pwr_op_alm_limit.insert(0, pwr_op_alm_limit)
    entry_pwr_op_alm_limit.bind('<Key-Return>', on_pwr_op_alm_limit_changed)

    button_save_close = tk.Button(    configwin, 
                            text="Save & Close", 
                            font=dfont,
                            command = configwin_save_close)
   
    label_con0.grid(row=1, column=1, sticky=tk.E)
    label_con1.grid(row=2, column=1, sticky=tk.E)
    label_con2.grid(row=3, column=1, sticky=tk.E)
    label_con3.grid(row=4, column=1, sticky=tk.E)
    label_con4.grid(row=5, column=1, sticky=tk.E)
    label_con5.grid(row=6, column=1, sticky=tk.E)
    label_con6.grid(row=7, column=1, sticky=tk.E)
    label_con7.grid(row=8, column=1, sticky=tk.E)
    label_con8.grid(row=9, column=1, sticky=tk.E)
    label_con9.grid(row=0, column=0, sticky=tk.E)
    label_con10.grid(row=11, column=3, sticky=tk.E)

    entry_update_interval.grid(row=2, column=2, sticky=tk.E)
    entry_max_elements.grid(row=4, column=2, sticky=tk.E)
    entry_pwr_op_on.grid(row=6, column=2, sticky=tk.E)
    entry_pwr_op_alm_limit.grid(row=8, column=2, sticky=tk.E)

    button_save_close.grid(row = 10, column = 1)
    
    canvas.draw()

#-----------------------------------------------------------------------------------------
# Button: Configwin Save & close button,
def configwin_save_close():

    print ("at configwin save & close")
    global update_interval           # Time (ms) between polling/animation updates
    global max_elements             # Maximum number of elements to store in plot lists
    global pwr_op_on                    # PID power base line must get above to turn on
    global pwr_op_alm_limit         # Max value PID ouput will get to before alarm shut down ( Heater not working)
    global entry_update_interval
    global entry_max_elements
    global entry_pwr_op_on
    global entry_pwr_op_alm_limit
    global configwin

    # get target value and error chk
    try:
        value = float(entry_update_interval.get())
        print(value)
        update_interval = value
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
  
    pass
    configwin.destroy()
        
#------------------------------------------------------------------------------------------
# Button: Help 
def help_window():

    print ('at help window')
    helpwin = tk.Toplevel(root)
    helpwin.geometry('950x900')
    helpwin.title("Help Window")
    msg = tk.Message(helpwin, text=helptxt, font = 12, width = 950)
    msg.pack()
    
#--------------------------------------------------------------------------------------
# Button: Toggle the PID Power plot
def toggle_Power():

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

#---------------------------------------------------------------------------------------
# Button: Toggle the temperature plot
def toggle_temp():

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

#-----------------------------------------------------------------------------
# Button: Toggel manual ctrl
def manual_ctrl():
    
    print("at manual_ctrl")
    global manual_state
    global led_manual
    global PID1_run_state
    global led_runpid1
    global PID2_run_state
    global led_runpid2
    global PID3_run_state
    global led_runpid3
    
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
    
    print("at heater1")
    global heater1_state
    global led_heater1

    if (manual_state == True):
        heater1_state = not heater1_state
        led_heater1. to_red(heater1_state)
    
        if (heater1_state == True):
            HEATER1.on()
        else:
            HEATER1.off()
  
        canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel heater2
def heater2():
    
    print("at heater2")
    global heater2_state
    global led_heater2

    if (manual_state == True):
        heater2_state = not heater2_state
        led_heater2. to_red(heater2_state)
    
        if (heater2_state == True):
            HEATER2.on()
        else:
            HEATER2.off()

        canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel heater3
def heater3():
    
    print("at heater3realy")
    global heater3_state
    global led_heater3
    
    if (manual_state == True):
        heater3_state = not heater3_state
        led_heater3. to_red(heater3_state)

        if (heater3_state == True):
            HEATER3.on()
        else:
            HEATER3.off()
        
        canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID1 Run
def PID1_run():
    
    print("at PID1_run")
    global PID1_run_state
    global manual_state
    global led_runpid1

    if (manual_state == False):
        PID1_run_state = not PID1_run_state
        led_runpid1. to_green(PID1_run_state)
        heater1_state = (False)
        led_heater1. to_red(heater1_state)
        HEATER1.off()

        if (PID1_run_state == True):        # restart PID, so reset variables
            r1=PID1_reset()
        
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID2 Run
def PID2_run():
    
    print("at PID2_run")
    global PID2_run_state
    global manual_state
    global led_runpid2

    if (manual_state == False):
        PID2_run_state = not PID2_run_state
        led_runpid2. to_green(PID2_run_state)
        heater2_state = (False)
        led_heater2. to_red(heater2_state)
        HEATER2.off()

        if (PID2_run_state == True):        # restart PID, so reset variables
            r2 = PID2_reset()
        
    canvas.draw()

#-----------------------------------------------------------------------------
# Button: Toggel PID3 Run
def PID3_run():
    
    print("at PID3_run")
    global PID3_run_state
    global manual_state
    global led_runpid3

    if (manual_state == False):
        PID3_run_state = not PID3_run_state
        led_runpid3. to_green(PID3_run_state)
        heater3_state = (False)
        led_heater3. to_red(heater3_state)
        HEATER3.off()

        if (PID3_run_state == True):        # restart PID, so reset variables
            r3 = PID3_reset()
        
    canvas.draw()

#---------------------------------------------------------------------------------------
# Entry: config window, update_interval value changed in GUI, Entry changed call back
def on_update_interval_changed(event):

    global update_interval           # Time (ms) between polling/animation updates

    # get target value and error chk
    try:
        value = float(entry_update_interval.get())
        print(value)
        update_interval = value
    except ValueError:
        print("Invalid Value in update_interval entry box")
    entry_update_interval.delete(0, 8)
    entry_update_interval.insert(0, update_interval)

    canvas.draw()

#---------------------------------------------------------------------------------------
# Entry: config window, max elements value changed in GUI, Entry changed call back
def on_max_elements_changed(event):

    global max_elements             # Maximum number of elements to store in plot lists
        
    # get target value and error chk
    try:
        value = int(entry_max_elements.get())
        print(value)
        max_elements = value
    except ValueError:
        print("Invalid Value in max_elements entry box")
    entry_max_elements.delete(0, 8)
    entry_max_elements.insert(0, max_elements)

    canvas.draw()
    
#---------------------------------------------------------------------------------------
# Entry: config window, base power output  value changed in GUI, Entry changed call back
def on_pwr_op_on_changed(event):

    global pwr_op_on                    # PID power base line must get above to turn on
    global entry_pwr_op_on
    
    # get target value and error chk
    try:
        value = int(entry_pwr_op_on.get())
        print(value)
        pwr_op_on = value
    except ValueError:
        print("Invalid Value in pwr_op_on entry box")
    entry_pwr_op_on.delete(0, 8)
    entry_pwr_op_on.insert(0, pwr_op_on)

    canvas.draw()
    
#---------------------------------------------------------------------------------------
# Entry: config window,  PID pwr out limit value changed in GUI, Entry changed call back
def on_pwr_op_alm_limit_changed(event):
    
    global pwr_op_alm_limit         # Max value PID ouput will get to before alarm shut down ( Heater not working)
    global entry_pwr_op_alm_limit
    
        # get target value and error chk
    try:
        value = int(entry_pwr_op_alm_limit.get())
        print(value)
        pwr_op_alm_limit = value
    except ValueError:
        print("Invalid Value in pwr_op_alm_limit entry box")
    entry_pwr_op_alm_limit.delete(0, 8)
    entry_pwr_op_alm_limit.insert(0, pwr_op_alm_limit)

    canvas.draw()
    
#---------------------------------------------------------------------------------------
# Entry: target1 value changed in GUI, Entry changed call back
def on_target1_changed(event):
    
    global target1                                          #target1 = 28
    
    # get target value and error chk
    try:
        value = float(entry_target1.get())
        print(value)
        target1 = value
    except ValueError:
        print("Invalid Value in Target 1 entry box")
    entry_target1.delete(0, 5)
    entry_target1.insert(0, target1)

    canvas.draw()

#------------------------------------------------------------------------------------
# Entry: P1 value changed in GUI, Entry changed call back
def on_P1_changed(event):
    
    global P1
    
    # get P1 value and error chk
    try:
        value = float(entry_P1.get())
        print(value)
        P1 = value
    except ValueError:
        print("Invalid Value in P1 entry box")
    entry_P1.delete(0, 5)
    entry_P1.insert(0, P1)

    canvas.draw()

#-----------------------------------------------------------------------------------
# Entry: I1 value changed in GUI, Entry changed call back
def on_I1_changed(event):
    
    global I1
    
    # get I1 value and error chk
    try:
        value = float(entry_I1.get())
        print(value)
        I1 = value
    except ValueError:
        print("Invalid Value in I1 entry box")
    entry_I1.delete(0, 5)
    entry_I1.insert(0, I1)

    canvas.draw()

#-----------------------------------------------------------------------------------
# Entry: D1 value changed in GUI, Entry changed call back
def on_D1_changed(event):
    
    global D1
    
    # get D1 value and error chk
    try:
        value = float(entry_D1.get())
        print(value)
        D1 = value
    except ValueError:
        print("Invalid Value in D1 entry box")
    entry_D1.delete(0, 5)
    entry_D1.insert(0, D1)

    canvas.draw()

#----------------------------------------------------------------------------------------
# Entry: target2 value changed in GUI, Entry changed call back
def on_target2_changed(event):
    
    global target2                                  #target1 = 28
    
    # get target value and error chk
    try:
        value = float(entry_target2.get())
        print(value)
        target2 = value
    except ValueError:
        print("Invalid Value in Target 2 entry box")
    entry_target2.delete(0, 5)
    entry_target2.insert(0, target2)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: P2 value changed in GUI, Entry changed call back
def on_P2_changed(event):
    
    global P2
    
    # get P2 value and error chk
    try:
        value = float(entry_P2.get())
        print(value)
        P2 = value
    except ValueError:
        print("Invalid Value in P2 entry box")
    entry_P2.delete(0, 5)
    entry_P2.insert(0, P2)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: I2 value changed in GUI, Entry changed call back
def on_I2_changed(event):
    
    global I2
    
    # get I2 value and error chk
    try:
        value = float(entry_I2.get())
        print(value)
        I2 = value
    except ValueError:
        print("Invalid Value in I2 entry box")
    entry_I2.delete(0, 5)
    entry_I2.insert(0, I2)

    canvas.draw()

#---------------------------------------------------------------------------------
# Entry: D2 value changed in GUI, Entry changed call back
def on_D2_changed(event):
    
    global D2
    
    # get D2 value and error chk
    try:
        value = float(entry_D2.get())
        print(value)
        D2 = value
    except ValueError:
        print("Invalid Value in D2 entry box")
    entry_D2.delete(0, 5)
    entry_D2.insert(0, D2)

    canvas.draw()

#-------------------------------------------------------------------------------------
# Entry: target3 value changed in GUI, Entry changed call back
def on_target3_changed(event):
    
    global target3                              #target1 = 28
    
    # get target value and error chk
    try:
        value = float(entry_target3.get())
        print(value)
        target3 = value
    except ValueError:
        print("Invalid Value in Target 3 entry box")
    entry_target3.delete(0, 5)
    entry_target3.insert(0, target3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: P3 value changed in GUI, Entry changed call back
def on_P3_changed(event):
    
    global P3
    
    # get P3 value and error chk
    try:
        value = float(entry_P3.get())
        print(value)
        P3 = value
    except ValueError:
        print("Invalid Value in P3 entry box")
    entry_P3.delete(0, 5)
    entry_P3.insert(0, P3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: I3 value changed in GUI, Entry changed call back
def on_I3_changed(event):
    
    global I3
    
    # get I3 value and error chk
    try:
        value = float(entry_I3.get())
        print(value)
        I3 = value
    except ValueError:
        print("Invalid Value in I3 entry box")
    entry_I3.delete(0, 5)
    entry_I3.insert(0, I3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: D3 value changed in GUI, Entry changed call back
def on_D3_changed(event):
    
    global D3
    
    # get D3 value and error chk
    try:
        value = float(entry_D3.get())
        print(value)
        D3 = value
    except ValueError:
        print("Invalid Value in D3 entry box")
    entry_D3.delete(0, 5)
    entry_D3.insert(0, D2)

    canvas.draw()
    


#-----------------------------------------------------------------------------
# PID1 reset every thing to off, include PID calcs and output, called at verious points
def PID1_reset():
    
    print("at PID1_Reset")
    global PID1_run_state
    global power1_state
    global heater1_state
    global error1
    global interror1
    global power1

    led_runpid1.to_green(PID1_run_state)
    power1_state = False
    led_pidop1.to_green(power1_state)
    error1 = 0
    interror1 = 0
    power1 = 0
    heater1_state = (False)
    led_heater1. to_red(heater1_state)
    HEATER1.off()
    led_alarm1.to_red(False)
    ALMBUZZER.off()
    
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
    ALMBUZZER.off()

#---------------------------------------------------------------------------------------
# Binding: Toggle fullscreen, triggered by pressing <F11>
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)   

#-------------------------------------------------------------------------------------
# Binding: Return to windowed mode, not used
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

#--------------------------------------------------------------------------------------
# Binding: Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 35)))
    dfont.configure(size=new_size)
    
#------------------------------------------------------------------------------------------------------    
# Binding: comes here to terminate GUI if <ESC> key pressed
def end(event):
    
    HEATER1.off()
    HEATER2.off()
    HEATER3.off()
    ALMBUZZER.off()
    pass
    root.destroy()

#-------------------------------------------------------------------------------------------------------
# Binding: Dummy function prevents segfault, clicking 'quit' comes here
def _destroy(event):
    
    HEATER1.off()
    HEATER2.off()
    HEATER3.off()
    ALMBUZZER.off()
    pass

#-----------------------------------------------------------------------------------------------------
# ANIMATE 
# It reads the Temperatures, does PID calc and turns Heatbands On/Off, alarms
# This function is called periodically from FuncAnimation
def animate(i, ax1, ax2, ax3, ax4, ax5, ax6, xs, temp1, temp2, temp3, Temp1GUI, Temp2GUI, Temp3GUI, pid1out, pid2out, pid3out, pid1GUI, pid2GUI, pid3GUI):

    # Update data to display temperature
    try:
        new_temp1= sensor1.readTempC()     #read SPI temp value
        new_temp2 = sensor2.readTempC()     #read SPI temp value
        new_temp3 = sensor3.readTempC()     #read SPI temp value
    except: 
        pass
        
    #point to global variables, and get value
    global pwr_op_alm_limit 
    global pwr_op_on
    
    global PID1_run_state
    global power1_state
    global PID1_alarm_state
    global target1
    global P1
    global I1
    global D1
    global error1
    global interror1
    global power1

    global PID2_run_state
    global power2_state
    global PID2_alarm_state
    global target2
    global P2
    global I2
    global D2
    global error2
    global interror2
    global power2

    global PID3_run_state
    global power3_state
    global PID3_alarm_state
    global target3
    global P3
    global I3
    global D3
    global error3
    global interror3
    global power3

    #PID1
    if (PID1_run_state == True):
        error1 = target1 - new_temp1
        interror1 = interror1 + error1
        power1 = D1 + ((P1 * error1) + ((I1 * interror1)))
        
        #if power > than base PID values turn output ON.  else turn output OFF
        if (power1 > pwr_op_on  ):
            print ("PID power1 ON")
            print()
            power1_state=True
            led_heater1.to_red(True)
            HEATER1.on()
        else:
            print ("PID power1 OFF")
            print ()
            power1_state=False
            led_heater1.to_red(False)
            HEATER1.off()
           
        led_pidop1.to_green(power1_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power1 > pwr_op_alm_limit):
            print ("PID1 ALARM")
            print ()
            PID1_run_state = False
            led_runpid1.to_green(False)
            led_heater1.to_red(False)
            HEATER1.off()
            led_alarm1.to_red(True)
            ALMBUZZER.on()
           
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
            led_heater2.to_red(True)
            HEATER2.on()
        else:
            print ("PID power2 OFF")
            print ()
            power2_state=False
            led_heater2.to_red(False)
            HEATER2.off()
           
        led_pidop2.to_green(power2_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power2 > pwr_op_alm_limit):
            print ("PID2 ALARM")
            print ()
            PID2_run_state = False
            led_runpid2.to_green(False)
            led_heater2.to_red(False)
            HEATER2.off()
            led_alarm2.to_red(True)
            ALMBUZZER.on()

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
            led_heater3.to_red(True)
            HEATER3.on()
        else:
            print ("PID power3 OFF")
            print ()
            power3_state=False
            led_heater3.to_red(False)
            HEATER3.off()
           
        led_pidop3.to_green(power3_state)

        # if power out > alarm limit shut down. Heaters not working
        if (power3 > pwr_op_alm_limit):
            print ("PID3 ALARM")
            print ()
            PID3_run_state = False
            led_runpid3.to_green(False)
            led_heater3.to_red(False)
            HEATER3.off()
            led_alarm3.to_red(True)
            ALMBUZZER.on()
    
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
    print ("Output on if > 10. Power1 Output =", power1)
    print()    
    print ("TARGET 2 TEMP =",target2)
    print ("P2 =",P2)
    print ("I2 =",I2)
    print ("D2 =",D2)
    print ("Error2 = target - temp =", error2)
    print ("Int Error2 = Int Error + Error =",interror2)
    print ()
    print ("Output on if > 10. Power2 Output =", power2)
    print ()
    print ("TARGET 3 TEMP =",target3)
    print ("P3 =",P3)
    print ("I3 =",I3)
    print ("D3 =",D3)
    print ("Error3 = target - temp =", error3)
    print ("Int Error3 = Int Error + Error =",interror3)
    print ()
    print ("Output on if > 10. Power3 Output =", power3)
    print ()
    print ("===========================================")

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
    
#==============================================================================


#------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main script
#------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create the main window
root = tk.Tk()
root.title("Zoe PID Controller")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg='white')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create figure for plotting
fig = figure.Figure(figsize=(2, 2))
fig.subplots_adjust(left=0.1, right=0.8)

   
# Create 3 x Graphs
ax1 = fig.add_subplot(3, 1, 1)
ax3 = fig.add_subplot(3, 1, 2)
ax5 = fig.add_subplot(3, 1, 3)

# fig.tight_layout()                               #this works but very small graphs

# Initiate a new set of axes that shares the same x-axis
ax2 = ax1.twinx()
ax4 = ax3.twinx()
ax6 = ax5.twinx()

# Empty x and y lists for storing data to plot later
xs = []
temp1 =[]
temp2 = []
temp3 = []
pid1out =[]
pid2out = []
pid3out = []

# Variables for holding temperature and PID data
Temp1GUI =tk.DoubleVar()
Temp2GUI = tk.DoubleVar()
Temp3GUI = tk.DoubleVar()
pid1GUI = tk.DoubleVar()
pid2GUI = tk.DoubleVar()
pid3GUI = tk.DoubleVar()

# Create dynamic font for text
dfont = tkFont.Font(size=-24)

# Create a Tk Canvas widget out of our figure
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_plot = canvas.get_tk_widget()

# Define other supporting widgets (labels,  Input entry, buttons, LEDS )
label_spacer1 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer3 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer4 = tk.Label(frame, text='   ', font=dfont, bg='white')

label_line1 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')
label_line2 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')
label_line3 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')

label_temp1 = tk.Label(frame, text='Temp 1 (Deg C):', font=dfont, bg='white')
label_celsius1 = tk.Label(frame, textvariable=Temp1GUI, font=dfont, bg='white')
label_target1 = tk.Label(frame, text='Target Temp 1: ', font=dfont, bg='white')
label_power1 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue1= tk.Label(frame, textvariable=pid1GUI, font=dfont, bg='white')
label_P1 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I1 = tk.Label(frame, text='I:' , font=dfont, bg='white')
label_D1 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout1 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
label_alarm1 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

label_temp2 = tk.Label(frame, text='Temp 2 (Deg C):', font=dfont, bg='white')
label_celsius2 = tk.Label(frame, textvariable=Temp2GUI, font=dfont, bg='white')
label_target2 = tk.Label(frame, text='Target Temp 2: ', font=dfont, bg='white')
label_power2 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue2= tk.Label(frame, textvariable=pid2GUI, font=dfont, bg='white')
label_P2 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I2 = tk.Label(frame, text='I: ', font=dfont, bg='white')
label_D2 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout2 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
label_alarm2 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

label_temp3 = tk.Label(frame, text='Temp 3 (Deg C):', font=dfont, bg='white')
label_celsius3 = tk.Label(frame, textvariable=Temp3GUI, font=dfont, bg='white')
label_target3 = tk.Label(frame, text='Target Temp 3: ', font=dfont, bg='white')
label_power3 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue3= tk.Label(frame, textvariable=pid3GUI, font=dfont, bg='white')
label_P3 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I3 = tk.Label(frame, text='I: ', font=dfont, bg='white')
label_D3 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout3 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
label_alarm3 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

#---- 1
sv = "StringVar()"
entry_target1 = tk.Entry(frame, textvariable = sv, font=dfont, bg='white',  width=5)
entry_target1.insert(0, target1)
entry_target1.bind('<Key-Return>', on_target1_changed)

entry_P1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_P1.insert(0, P1)
entry_P1.bind('<Key-Return>', on_P1_changed)

entry_I1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_I1.insert(0, I1)
entry_I1.bind('<Key-Return>', on_I1_changed)

entry_D1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_D1.insert(0, D1)
entry_D1.bind('<Key-Return>', on_D1_changed)

#------ 2
entry_target2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_target2.insert(0, target2)
entry_target2.bind('<Key-Return>', on_target2_changed)

entry_P2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_P2.insert(0, P2)
entry_P2.bind('<Key-Return>', on_P2_changed)

entry_I2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_I2.insert(0, I2)
entry_I2.bind('<Key-Return>', on_I2_changed)

entry_D2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_D2.insert(0, D2)
entry_D2.bind('<Key-Return>', on_D2_changed)

#----- 3
entry_target3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_target3.insert(0, target3)
entry_target3.bind('<Key-Return>', on_target3_changed)

entry_P3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_P3.insert(0, P3)
entry_P3.bind('<Key-Return>', on_P3_changed)

entry_I3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_I3.insert(0, I3)
entry_I3.bind('<Key-Return>', on_I3_changed)

entry_D3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_D3.insert(0, D3)
entry_D3.bind('<Key-Return>', on_D3_changed)

#-------------------------------------------------------------------------------
button_save_file = tk.Button(    frame, 
                            text="Save As...", 
                            font=dfont,
                            command= save_file)

button_load_file = tk.Button(    frame, 
                            text="Load...", 
                            font=dfont,
                            command= load_file)

button_config = tk.Button(    frame, 
                            text="Config...", 
                            font=dfont,
                            command= config)

button_help = tk.Button(    frame,
                            text="Help",
                            font=dfont,
                            command=help_window)

button_runpid1 = tk.Button(    frame, 
                            text="PID1 Run", 
                            font=dfont,
                            command=PID1_run)

button_runpid2 = tk.Button(   frame,
                            text="PID2 Run",
                            font=dfont,
                            command=PID2_run)

button_runpid3 = tk.Button(    frame,
                            text="PID3 Run",
                            font=dfont,
                            command=PID3_run)

button_pid = tk.Button(   frame,
                            text="Toggle PID",
                            font=dfont,
                            command=toggle_Power)

button_temp = tk.Button(    frame, 
                            text="Toggle Temp", 
                            font=dfont,
                            command=toggle_temp)

button_manual = tk.Button(    frame, 
                            text="Manual", 
                            font=dfont,
                            command=manual_ctrl)

button_heater1 = tk.Button(   frame,
                            text="Heater 1",
                            font=dfont,
                            command=heater1)

button_heater2 = tk.Button(    frame,
                            text="Heater 2",
                            font=dfont,
                            command=heater2)

button_heater3 = tk.Button(    frame,
                            text="Heater 3",
                            font=dfont,
                            command=heater3)

button_quit = tk.Button(    frame,
                            text="Quit",
                            font=dfont,
                            command=root.destroy)

#led0 = tk_tools.Led(root, size=50, on_click_callback=on_click_callback)
led_runpid1 = tk_tools.Led(frame, size=25)
led_pidop1 = tk_tools.Led(frame, size=25)
led_alarm1 = tk_tools.Led(frame, size=25)
led_runpid1.to_green()
led_pidop1.to_green()
led_alarm1.to_red()

led_runpid2 = tk_tools.Led(frame, size=25)
led_pidop2 = tk_tools.Led(frame, size=25)
led_alarm2 = tk_tools.Led(frame, size=25)
led_runpid2.to_green()
led_pidop2.to_green()
led_alarm2.to_red()

led_runpid3 = tk_tools.Led(frame, size=25)
led_pidop3 = tk_tools.Led(frame, size=25)
led_alarm3 = tk_tools.Led(frame, size=25)
led_runpid3.to_green()
led_pidop3.to_green()
led_alarm3.to_red()

led_manual =  tk_tools.Led(frame, size=25)
led_heater1 = tk_tools.Led(frame, size=25)
led_heater2 = tk_tools.Led(frame, size=25)
led_heater3 = tk_tools.Led(frame, size=25)
led_manual.to_red() 
led_heater1.to_red()
led_heater2.to_red()
led_heater3.to_red()

# The three geometry managers are: grid, pack, and place.
# You should never mix geometry managers within the same hierarchy, but you can embed different
# managers within each other (for example, you can lay out a frame widget with grid in a Toplevel and
# then use pack to put different widgets within the frame).
#
# Lay out widgets in a grid in the frame. GRID is 11 colums (0-10) x 14 rows (0-13)
#
# this is the plot, starts at 0,0 spans 5 rows (down) and spans  5 colums (across)
canvas_plot.grid(   row=0, 
                    column=0, 
                    rowspan=14, 
                    columnspan=5, 
                    sticky=tk.W+tk.E+tk.N+tk.S)

# Poistion Widgets on grid
#Example:-
#label_temp1.grid(row=1, column=3, padx=100, pady=50, columnspan=2, sticky=tk.W)       

# row 0 options
label_spacer1.grid(row = 0 , column = 0)
button_save_file.grid(row = 0, column = 8)
button_load_file.grid(row = 0 , column  = 7)
button_config.grid(row = 0, column = 9)
button_help.grid (row = 0, column = 10)

#row 1 PID1
label_temp1.grid(row=1, column=5)
label_celsius1.grid(row=1, column=6, sticky=tk.W)
label_P1.grid(row=1, column=7, sticky=tk.E)
entry_P1.grid(row=1, column=8, sticky=tk.W)
button_runpid1.grid (row = 1, column = 9)
led_runpid1.grid(row=1, column = 10)

#row 2 PID1
label_target1.grid(row=2, column=5, sticky=tk.E)
entry_target1.grid(row=2, column=6, sticky=tk.W)
label_I1.grid(row=2, column=7, stick=tk.E)
entry_I1.grid(row=2, column= 8, sticky =tk.W)
label_pidout1.grid(row=2,  column = 9,sticky=tk.E)
led_pidop1.grid(row=2, column = 10)

#row 3 PID1
label_power1.grid(row=3, column=5, sticky=tk.E)
label_powervalue1.grid(row=3, column=6, stick=tk.W)
label_D1.grid(row=3, column=7, sticky=tk.E)                
entry_D1.grid(row=3, column=8, sticky=tk.W)
label_alarm1.grid(row=3, column=9, sticky=tk.E)
led_alarm1.grid(row=3, column = 10)

#row 4 - line
label_line1.grid(row=4, column=5, columnspan=6, sticky=tk.W)

#row 5 PID2
label_temp2.grid(row=5, column=5)
label_celsius2.grid(row=5, column=6, sticky=tk.W)
label_P2.grid(row=5, column=7, sticky=tk.E)
entry_P2.grid(row=5, column=8, sticky=tk.W)
button_runpid2.grid (row = 5, column = 9)
led_runpid2.grid(row=5, column = 10)

#row 6 PID 2
label_target2.grid(row=6, column=5, sticky=tk.E)
entry_target2.grid(row=6, column=6, sticky=tk.W)
label_I2.grid(row=6, column=7, sticky=tk.E)
entry_I2.grid(row=6, column= 8, sticky=tk.W)
label_pidout2.grid(row=6,  column = 9, sticky=tk.E)
led_pidop2.grid(row=6, column = 10)

#row 7 PID 2
label_power2.grid(row=7, column=5, sticky=tk.E)
label_powervalue2.grid(row=7, column=6, sticky=tk.W)
label_D2.grid(row=7, column=7, sticky=tk.E)                
entry_D2.grid(row=7, column=8, sticky=tk.W)
label_alarm2.grid(row=7, column=9,sticky=tk.E)
led_alarm2.grid(row=7, column = 10)

#row 8 - line
label_line2.grid(row=8, column=5, columnspan=6, sticky=tk.W)

#row 9 PID3
label_temp3.grid(row=9, column=5)
label_celsius3.grid(row=9, column=6, sticky=tk.W)
label_P3.grid(row=9, column=7, sticky=tk.E)
entry_P3.grid(row=9, column=8, sticky=tk.W)
button_runpid3.grid (row = 9, column = 9)
led_runpid3.grid(row=9, column = 10)

#row 10
label_target3.grid(row=10, column=5, sticky=tk.E)
entry_target3.grid(row=10, column=6, sticky=tk.W)
label_I3.grid(row=10, column=7,  sticky=tk.E)
entry_I3.grid(row=10, column= 8,  sticky=tk.W)
label_pidout3.grid(row=10,  column = 9, sticky=tk.E)
led_pidop3.grid(row=10, column = 10)

#row 11
label_power3.grid(row=11, column=5, sticky=tk.E)
label_powervalue3.grid(row=11, column=6, sticky=tk.W)
label_D3.grid(row=11, column=7, sticky=tk.E)                
entry_D3.grid(row=11, column=8, sticky= tk.W)
label_alarm3.grid(row=11, column=9,sticky=tk.E)
led_alarm3.grid(row=11, column = 10)

#row 12 - line
label_line3.grid(row=12, column=5, columnspan=6, sticky=tk.W)

#row 13   
button_pid.grid(row=13, column=0)
button_temp.grid(row=13, column=1)
button_manual.grid(row=13, column=2,sticky = tk.E)
led_manual.grid(row=13, column = 3, sticky=tk.W)
button_heater1.grid(row=13, column=4, sticky=tk.E)
led_heater1.grid(row=13, column = 5, sticky=tk.W)
button_heater2.grid(row=13, column=6, sticky=tk.E)
led_heater2.grid(row=13, column = 7, sticky=tk.W)
button_heater3.grid(row=13, column=8, sticky=tk.E)
led_heater3.grid(row=13, column=9, sticky= tk.W)
button_quit.grid(row=13, column=10, sticky = tk.E)

# row 14 - corner padding
label_spacer3.grid(row = 14, column = 0)
label_spacer4.grid(row = 14, column = 10)

#----------------------------------------------------------------------------------------------
# Add a standard 5 pixel padding to all widgets
#for w in frame.winfo_children():
#   w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 14):
    frame.rowconfigure(i, weight=1)
for i in range(0, 10):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end program
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end)                  

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit, 'quit' clicked, to prevent segmentation fault
root.bind("<Destroy>", _destroy)

# Call animate() function periodically. this does the temperature measurment and PID calc
fargs = (ax1, ax2, ax3, ax4, ax5, ax6, xs, temp1, temp2, temp3, Temp1GUI, Temp2GUI, Temp3GUI, pid1out, pid2out, pid3out, pid1GUI, pid2GUI, pid3GUI)
ani = animation.FuncAnimation(  fig, 
                                animate, 
                                fargs=fargs, 
                                interval=update_interval)               

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()

