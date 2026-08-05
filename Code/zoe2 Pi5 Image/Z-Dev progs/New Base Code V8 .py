#4-9-2020
# New Base Code V8
#
# Original code Source
# https://www.digikey.co.uk/en/maker/projects/python-gui-guide-introduction-to-tkinter/d04a764c78114682aac9255056026338

# <ESC>  end GUI
# <F1> Help window, explain active keys and how buttons work
# <F11> Toggel full screen


# Goals :-
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

#To Do
# link entry values to PID variables
# link PID OP to heaters
# link maual override
# alarm & buzzer function
# write event log to disk file, alarms etc
# help window

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

#from time import sleep
import datetime as dt

#--------------------------------------------------------------------------------------------------------
# Config GPIO H/W pin asignment, using GPIO labeling, not pin header
HEATER1 = LED(27)
HEATER2 = LED(23)
HEATER3 = LED(22)
ALMBUZZER = LED(24)

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
update_interval = 1000 # Time (ms) between polling/animation updates(read temps and update PID)
max_elements = 1440     # Maximum number of elements to store in plot lists

# Initialise PID variables 
target1 = 28
target2 = 28
target3 = 28
P1 = 1
P2 = 1
P3 = 1
I1 = 1
I2 = 1
I3 = 1
D1= 0
D2 = 0
D3 = 0

interror1 = 0
error1 = 0
power1 = 0

interror2 = 0
error2 = 0
power2 = 0

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
PID1_run_state = None
PID2_run_state = None
PID3_run_state = None
manual_state = None
heater1_state = None
heater2_state = None
heater3_state = None

# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
Power_plot_visible = True
PID1_run_state = False
PID1_run_state = False
PID2_run_state = False
PID3_run_state = False
manual_state = False
heater1_state = False
heater2_state = False
heater3_state = False



###############################################################################
# Functions
#--------------------------------------------------------------
# Toggle fullscreen, triggered by pressing <F11>
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)   

#---------------------------------------------------------------
# Return to windowed mode, not used
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

#----------------------------------------------------------------------------------
# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 35)))
    dfont.configure(size=new_size)

#------------------------------------------------------------------------------------
# Toggle the temperature plot
def toggle_temp():

    global canvas
    global ax1
    global ax3
    global ax5
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

#---------------------------------------------------------------------------------
# Toggle the Power plot
def toggle_Power():

    global canvas
    global ax2
    global ax4
    global ax6
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

#-----------------------------------------------------------------------------
# Button Toggel PID1 Run
def PID1_run(): 
    global PID1_run_state
    global led_runpid1

    PID1_run_state = not PID1_run_state
    led_runpid1. to_green(PID1_run_state)

    
    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel PID2 Run
def PID2_run():
    print("at PID2_run")
    global PID2_run_state
    global led_runpid2

    PID2_run_state = not PID2_run_state
    led_runpid2. to_green(PID2_run_state)

    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel PID3 Run
def PID3_run():
    print("at PID3_run")
    global PID3_run_state
    global led_runpid3

    PID3_run_state = not PID3_run_state
    led_runpid3. to_green(PID3_run_state)

    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel manual ctrl
def manual_ctrl():
    print("at manual_ctrl")
    global manual_state
    global led_manual

    manual_state = not manual_state
    led_manual. to_red(manual_state)

    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel heater1
def heater1():
    print("at heater1")
    global heater1_state
    global led_heater1

    heater1_state = not heater1_state
    led_heater1. to_red(heater1_state)
    
    if (heater1_state == True):
        HEATER1.on()
    else:
        HEATER1.off()
  
    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel heater2
def heater2():
    print("at heater2")
    global heater2_state
    global led_heater2

    heater2_state = not heater2_state
    led_heater2. to_red(heater2_state)
    
    if (heater2_state == True):
        HEATER2.on()
    else:
        HEATER2.off()

    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel heater3
def heater3():
    print("at heater3")
    global heater3_state
    global led_heater3

    heater3_state = not heater3_state
    led_heater3. to_red(heater3_state)

    if (heater3_state == True):
        HEATER3.on()
    else:
        HEATER3.off()
        
    canvas.draw()

#-----------------------------------------------------------------------------
# Button Toggel help window 
def help_window(): 
    print("at help")
    
# comes here to terminate GUI if <ESC> key pressed
def end(event):
    pass
    root.destroy()

# Dummy function prevents segfault
def _destroy(event):
    pass

#-----------------------------------------------------------------------------------------------------
# MAIN PROCESSING Engine. It reads the Temperatures, does PID calc and turns Heatbands On/Off, alarms
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
    global target1
    global P1
    global I1
    global D1
    global error1
    global interror1
    global power1

    global target2
    global P2
    global I2
    global D2
    global error2
    global interror2
    global power2

    global target3
    global P3
    global I3
    global D3
    global error3
    global interror3
    global power3

    #PID1
    error1 = target1 - new_temp1
    interror1 = interror1 + error1
    power1 = D1 + ((P1 * error1) + ((I1 * interror1)))

    #PID2
    error2 = target2 - new_temp2
    interror2 = interror2 + error2
    power2 = D2 + ((P2 * error2) + ((I2 * interror2)))

    #PID3
    error3 = target3 - new_temp3
    interror3 = interror3 + error3
    power3 = D3 + ((P3 * error3) + ((I3 * interror3)))

    print ("**********Entering PID control loop****************")
    print ()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(new_temp1, new_temp2, new_temp3))
    print ()
    print ("TARGET 1 TEMP =",target1)
    print ("TARGET 2 TEMP =",target2)
    print ("TARGET 3 TEMP =",target3)
    print ()
    print ("P1 =",P1)
    print ("I1 =",I1)
    print ("D1 =",D1)
    print ()
    print ("Error1 = target - temp =", error1)
    print ("Int Error1 = Int Error + Error =",interror1)
    print ()
    print ('Output on if > 10')
    print()
    print ("Power1 Output =", power1)
    print ("Power2 Output =", power2)
    print ("Power3 Output =", power3)
    print ()
    print ("=============================")

    '''
    # Make sure that if power should be off then it is
    if (state=="off"):
        turn_off()
        print ("Pwr saftey set to Off")
        print ()
    #if power > than base PID values turn output ON.  else turn output OFF
    if (power>10  ):
        print ("PID power ON")
        print()
        state="on"
        turn_on()
    else:
        print ("PID power OFF")
        print ()
        state="off"
        turn_off()

    print ("state=", state)
    '''

    # Update our labels on GUI page. Does not mean graphs. May not need pid1GUI as power1 is global
    Temp1GUI.set(new_temp1)
    Temp2GUI.set(new_temp2)
    Temp3GUI.set(new_temp3)
    pid1GUI.set(power1)
    pid2GUI.set(power2)
    pid3GUI.set(power3)
        
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
    # Clear, format, and plot Temp1 values first (behind)
    color = 'tab:blue'
    ax1.clear()
    ax1.set_ylabel('PID 1', color=color)
    #ax1.set_xlim(15,40)                 # fix auto scale and set Temperature scale, not working
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.plot(xs, pid1out, linewidth=2, color=color)
    
    
    # This fulls the plot in. down to zero, is quite nice. works with ax1.collections lines
    #ax1.fill_between(xs, temp1, 0, linewidth=2, color=color, alpha=0.3)
    #ax1.fill_between(xs, temp1, linewidth=2, color=color, alpha=0.3)
    
    # Clear, format, and plot pid1out values (in front)
    color = 'tab:red'
    ax2.clear()
    ax2.set_ylabel('Temperature 1 (C)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(xs, temp1, linewidth=2, color=color)
    
    #-------------------------------  Graph 2 Temp2 PID OP2 --------------------------------------------
    # Clear, format, and plot Temp2 values first (behind)
    color = 'tab:blue'
    ax3.clear()
    ax3.set_ylabel('PID 2', color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.plot(xs, pid2out, linewidth=2, color=color)

    # Clear, format, and plot pid2out values (in front)
    color = 'tab:red'
    ax4.clear()
    ax4.set_ylabel('Temperature 2 (C)', color=color)
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.plot(xs, temp2, linewidth=2, color=color)
    
    #---------------------------------  Graph 3 Temp 3 PID OP3 ------------------------------------------
    # Clear, format, and plot Temp3 values first (behind)
    color = 'tab:blue'
    ax5.clear()
    ax5.set_ylabel('PID 3', color=color)
    ax5.tick_params(axis='y', labelcolor=color)
    ax5.plot(xs, pid3out, linewidth=2, color=color)

    # Clear, format, and plot pid3out values (in front)
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
    ax1.get_lines()[0].set_visible(temp_plot_visible)
    ax2.get_lines()[0].set_visible(Power_plot_visible)
    ax3.get_lines()[0].set_visible(temp_plot_visible)
    ax4.get_lines()[0].set_visible(Power_plot_visible)
    ax5.get_lines()[0].set_visible(temp_plot_visible)
    ax6.get_lines()[0].set_visible(Power_plot_visible)

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
label_spacer2 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer3 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer4 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer5 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_spacer6 = tk.Label(frame, text='   ', font=dfont, bg='white')
label_temp1 = tk.Label(frame, text='Temp 1 (Deg C):', font=dfont, bg='white')
label_celsius1 = tk.Label(frame, textvariable=Temp1GUI, font=dfont, bg='white')
label_target1 = tk.Label(frame, text='Target Temp 1: ', font=dfont, bg='white')
label_power1 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue1= tk.Label(frame, textvariable=pid1GUI, font=dfont, bg='white')
label_P1 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I1 = tk.Label(frame, text='I:' , font=dfont, bg='white')
label_D1 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout1 = tk.Label(frame, text='PID P/O: ', font=dfont, bg='white')
label_alarm1 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

label_temp2 = tk.Label(frame, text='Temp 2 (Deg C):', font=dfont, bg='white')
label_celsius2 = tk.Label(frame, textvariable=Temp2GUI, font=dfont, bg='white')
label_target2 = tk.Label(frame, text='Target Temp 2: ', font=dfont, bg='white')
label_power2 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue2= tk.Label(frame, textvariable=pid2GUI, font=dfont, bg='white')
label_P2 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I2 = tk.Label(frame, text='I: ', font=dfont, bg='white')
label_D2 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout2 = tk.Label(frame, text='PID P/O: ', font=dfont, bg='white')
label_alarm2 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

label_temp3 = tk.Label(frame, text='Temp 3 (Deg C):', font=dfont, bg='white')
label_celsius3 = tk.Label(frame, textvariable=Temp3GUI, font=dfont, bg='white')
label_target3 = tk.Label(frame, text='Target Temp 3: ', font=dfont, bg='white')
label_power3 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
label_powervalue3= tk.Label(frame, textvariable=pid3GUI, font=dfont, bg='white')
label_P3 = tk.Label(frame, text='P: ', font=dfont, bg='white')
label_I3 = tk.Label(frame, text='I: ', font=dfont, bg='white')
label_D3 = tk.Label(frame, text='D: ', font=dfont, bg='white')
label_pidout3 = tk.Label(frame, text='PID P/O: ', font=dfont, bg='white')
label_alarm3 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

entry_target1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_P1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_I1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_D1 = tk.Entry(frame, font=dfont, bg='white',  width=5)

entry_target2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_P2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_I2 = tk.Entry(frame, font=dfont, bg='white', width=5)
entry_D2 = tk.Entry(frame, font=dfont, bg='white', width=5)

entry_target3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_P3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_I3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
entry_D3 = tk.Entry(frame, font=dfont, bg='white',  width=5)

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
button_help = tk.Button(    frame,
                            text="Help",
                            font=dfont,
                            command=help_window)
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
# 
# Lay out widgets in a grid in the frame. GRID is 11 colums (0-10) x 14 rows (0-13)
# this is the plot, starts at 0,0 spans 5 rows (down) and spans  5 colums (across)
canvas_plot.grid(   row=0, 
                    column=0, 
                    rowspan=14, 
                    columnspan=5, 
                    sticky=tk.W+tk.E+tk.N+tk.S)

# Poistion Widgets on grid
#Example:-
#label_temp1.grid(row=1, column=3, padx=100, pady=50, columnspan=2, sticky=tk.W)       

# corner padding
label_spacer1.grid(row = 0 , column = 0)
label_spacer2.grid(row = 0, column = 10)
label_spacer3.grid(row = 14, column = 0)
label_spacer4.grid(row = 14, column = 10)

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

#row 4 - blank

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

#row 8 - blank
label_spacer5.grid(row=8, column=10)

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

#row 12 - blank
label_spacer6.grid(row=12, column=10)

#row 13   
button_pid.grid(row=13, column=0)
button_temp.grid(row=13, column=1)
button_manual.grid(row=13, column=2,sticky = tk.E)
led_manual.grid(row=13, column = 3, sticky=tk.W)
button_heater1.grid(row=13, column=4, sticky=tk.E)
led_heater1.grid(row=13, column = 5, sticky=tk.W)
button_heater2.grid(row=13, column=6, sticky=tk.W)
led_heater2.grid(row=13, column = 7, sticky=tk.E)
button_heater3.grid(row=13, column=8, sticky=tk.E)
led_heater3.grid(row=13, column=9, sticky= tk.W)
button_quit.grid(row=13, column=10, sticky = tk.W)

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

# Call empty _destroy function on exit to prevent segmentation fault
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


'''
# Get PID inputs
target1 = input('Enter Target Temperature, DegC : ')
if (target1 == ""):
    target1 = 28
    target2 = 28
    target3 = 28
target1 = int(target1)
print ('Target Temperature is: %d' % (target1))
print ()

P1 = input('Enter P value: ')
if (P1==""):
  P1 = 1
  P2 = 1
  P3 = 1
P1= int(P1)
print ('P = ',P1)
print ()

I1 = input('Enter I value: ')
if (I1==""):
   I1 = 1
   I2 = 1
   I3 = 1
I1 = int(I1)
print ('I = ',I1)
print ()

D1 = input ('Enter I value: ')
if (D1 == ""):
  D1= 0
  D2 = 0
  D3 = 0
D1 = int(D1)
print ('D = ',D1)
print ()
'''
