
# New Base Code V4
# Source
# https://www.digikey.co.uk/en/maker/projects/python-gui-guide-introduction-to-tkinter/d04a764c78114682aac9255056026338
# <F11> return to full screen
# <ESC> close full screen

# Goal :- Get 3 x graphs up -DONE
# tidy up graphs. Max min, add PID data



import datetime as dt
import tkinter as tk
import tkinter.font as tkFont

import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

###############################################################################
# Parameters and global variables

# Parameters
update_interval = 1000 # Time (ms) between polling/animation updates
max_elements = 1440     # Maximum number of elements to store in plot lists

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None      # Axis Temperature 1
ax2 = None      # Axis PID1_Out
ax3 = None      #Axis Temperature 2
ax4 = None      #Axis PID2_Out
ax5 = None      #Axis Temperature 3
ax6 = None      #Axis PID3_Out
temp_plot_visible = None


# Global variable to remember various states
fullscreen = False
temp_plot_visible = True
Power_plot_visible = True

# GPIO pin asignment, using GPIO labeling, not pin header
CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15

#HEATER1 = 27
#HEATER2 = 22
#HEATER3 = 23

# SPI MAX6675 software configuration (temperature Sensors)
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)


###############################################################################
# Functions
#--------------------------------------------------------------
# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)   

#---------------------------------------------------------------
# Return to windowed mode
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
    #new_size = -max(12, int((frame.winfo_height() / 15)))      #orignal code
    new_size = -max(12, int((frame.winfo_height() / 30)))
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
    ax1.get_lines()[0].set_visible(temp_plot_visible)
    ax1.get_yaxis().set_visible(temp_plot_visible)
    ax3.get_lines()[0].set_visible(temp_plot_visible)
    ax3.get_yaxis().set_visible(temp_plot_visible)
    ax5.get_lines()[0].set_visible(temp_plot_visible)
    ax5.get_yaxis().set_visible(temp_plot_visible)
  
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
    ax2.get_lines()[0].set_visible(Power_plot_visible)
    ax2.get_yaxis().set_visible(Power_plot_visible)
    ax4.get_lines()[0].set_visible(Power_plot_visible)
    ax4.get_yaxis().set_visible(Power_plot_visible)
    ax6.get_lines()[0].set_visible(Power_plot_visible)
    ax6.get_yaxis().set_visible(Power_plot_visible)
    
    canvas.draw()

# ----------------------- This function is called periodically from FuncAnimation-----------------------------------------
# this bit is the main Engine. It reads the Temperatures, does PID calc and turns Heatbands On/Off
#def animate(i, ax1, ax2, xs, temps, lights, temp_c, lux):
def animate(i, ax1, ax2, ax3, ax4, ax5, ax6, xs, temp1, temp2, temp3, Temp1GUI, Temp2GUI, Temp3GUI, pid1out, pid2out, pid3out, pid1GUI, pid2GUI, pid3GUI):

    # Update data to display temperature
    try:
        new_temp1= sensor1.readTempC()     #read SPI temp value
        new_temp2 = sensor2.readTempC()     #read SPI temp value
        new_temp3 = sensor3.readTempC()     #read SPI temp value
        #ERROR: print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp1, temp2, temp3))
             
    except: 
        pass
    
    # do PID here to
    new_pid1 = int(23)
    new_pid2 = int(40)
    new_pid3 = int(67)

    # Update our labels on GUI page. Does not mean graphs
    Temp1GUI.set(new_temp1)
    Temp2GUI.set(new_temp2)
    Temp3GUI.set(new_temp3)
    pid1GUI.set(new_pid1)
    pid2GUI.set(new_pid2)
    pid3GUI.set(new_pid3)
    
    
    # Append timestamp to x-axis list
    timestamp = mdates.date2num(dt.datetime.now())
    xs.append(timestamp)

    # this is our data arrays
    # Append sensor data to lists for plotting
    temp1.append(new_temp1)
    temp2.append(new_temp2)
    temp3.append(new_temp3)
    pid1out.append(new_pid1)
    pid2out.append(new_pid2)
    pid3out.append(new_pid3)
    
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
    color = 'tab:red'
    ax1.clear()
    ax1.set_ylabel('Temperature 1 (C)', color=color)
    #ax1.set_xlim(15,40)                 # fix auto scale and set Temperature scale, not working
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.plot(xs, temp1, linewidth=2, color=color)
    
    
    #this fulls the plot in. down to zero is quite nice. works with ax1.collections lines
    #ax1.fill_between(xs, temp1, 0, linewidth=2, color=color, alpha=0.3)
    #ax1.fill_between(xs, temp1, linewidth=2, color=color, alpha=0.3)
    
    # Clear, format, and plot pid1out values (in front)
    color = 'tab:blue'
    ax2.clear()
    ax2.set_ylabel('PID 1', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(xs, pid1out, linewidth=2, color=color)
    
    #-------------------------------  Graph 2 Temp2 PID OP2 --------------------------------------------
    # Clear, format, and plot Temp2 values first (behind)
    color = 'tab:red'
    ax3.clear()
    ax3.set_ylabel('Temperature 2 (C)', color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.plot(xs, temp2, linewidth=2, color=color)

    # Clear, format, and plot pid2out values (in front)
    color = 'tab:blue'
    ax4.clear()
    ax4.set_ylabel('PID 2', color=color)
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.plot(xs, pid2out, linewidth=2, color=color)
    
    #---------------------------------  Graph 3 Temp 3 PID OP3 ------------------------------------------
    # Clear, format, and plot Temp3 values first (behind)
    color = 'tab:red'
    ax5.clear()
    ax5.set_ylabel('Temperature 3 (C)', color=color)
    ax5.tick_params(axis='y', labelcolor=color)
    ax5.plot(xs, temp3, linewidth=2, color=color)

    # Clear, format, and plot pid3out values (in front)
    color = 'tab:blue'
    ax6.clear()
    ax6.set_ylabel('PID 3', color=color)
    ax6.tick_params(axis='y', labelcolor=color)
    ax6.plot(xs, pid3out, linewidth=2, color=color)

    #-----------------------------------------------------------------------------------------
    # Format timestamps to be more readable
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()
  
    # Make sure plots stay visible or invisible as desired
    #ax1.collections[0].set_visible(temp_plot_visible)      #to do with if theres a fill under the line 
    ax1.get_lines()[0].set_visible(temp_plot_visible)
    ax2.get_lines()[0].set_visible(Power_plot_visible)
    ax3.get_lines()[0].set_visible(temp_plot_visible)
    ax4.get_lines()[0].set_visible(Power_plot_visible)
    ax5.get_lines()[0].set_visible(temp_plot_visible)
    ax6.get_lines()[0].set_visible(Power_plot_visible)
    

# Dummy function prevents segfault
def _destroy(event):
    pass

###############################################################################
# Main script

# Create the main window
root = tk.Tk()
root.title("Sensor Dashboard")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg='white')

# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# Create figure for plotting
fig = figure.Figure(figsize=(2, 2))
fig.subplots_adjust(left=0.1, right=0.8)

   
# Create 3 x Graphs
#ax1 = fig.add_subplot(1, 1, 1)         #Original code, one graph
ax1 = fig.add_subplot(3, 1, 1)
#ax2 = None                                          #second axis on first graph
ax3 = fig.add_subplot(3, 1, 2)
#ax4 = None                                          # second axis on second graph
ax5 = fig.add_subplot(3, 1, 3)
#ax6 = None                                          #second axis on thrid graph

# fig.tight_layout()                               #this works but very small graphs

# Instantiate a new set of axes that shares the same x-axis
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

# Create other supporting widgets
label_temp1 = tk.Label(frame, text='Temperature 1:', font=dfont, bg='white')
label_celsius1 = tk.Label(frame, textvariable=Temp1GUI, font=dfont, bg='white')
label_unitc1 = tk.Label(frame, text="C", font=dfont, bg='white')             #puts a C after the temp value

label_temp2 = tk.Label(frame, text="Temperature 2:", font=dfont, bg='white')
label_celsius2 = tk.Label(frame, textvariable=Temp2GUI, font=dfont, bg='white')
label_unitc2 = tk.Label(frame, text="C", font=dfont, bg='white')

label_temp3 = tk.Label(frame, text="Temperature 3:", font=dfont, bg='white')
label_celsius3 = tk.Label(frame, textvariable=Temp3GUI, font=dfont, bg='white')
label_unitc3 = tk.Label(frame, text="C", font=dfont, bg='white')

button_temp = tk.Button(    frame, 
                            text="Toggle Temperature", 
                            font=dfont,
                            command=toggle_temp)
button_pid = tk.Button(   frame,
                            text="Toggle PID",
                            font=dfont,
                            command=toggle_Power)
button_quit = tk.Button(    frame,
                            text="Quit",
                            font=dfont,
                            command=root.destroy)

# Lay out widgets in a grid in the frame
# this grid method seams hard to control may need to change to pixels

canvas_plot.grid(   row=0, 
                    column=0, 
                    rowspan=5, 
                    columnspan=4, 
                    sticky=tk.W+tk.E+tk.N+tk.S)

#label_temp1.grid(row=1, column=3, padx=100, columnspan=2, sticky=tk.W)
label_temp1.grid(row=1, column=4, padx=100)
label_celsius1.grid(row=1, column=5, sticky=tk.W)
label_unitc1.grid(row=1, column=6, sticky=tk.W)

label_temp2.grid(row=2, column=4, columnspan=2)
label_celsius2.grid(row=2, column=5, sticky=tk.E)
label_unitc2.grid(row=2, column=6, sticky=tk.W)

label_temp3.grid(row=3, column=4, columnspan=2)
label_celsius3.grid(row=3, column=5, sticky=tk.E)
label_unitc3.grid(row=3, column=6, sticky=tk.W)

button_temp.grid(row=5, column=0, columnspan=2)
button_pid.grid(row=5, column=2, columnspan=2)
button_quit.grid(row=5, column=4, columnspan=2)

# Add a standard 5 pixel padding to all widgets
#for w in frame.winfo_children():
#   w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 5):
    frame.rowconfigure(i, weight=1)
for i in range(0, 5):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)
root.bind('<F1>', _destroy)     #does not work

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit to prevent segmentation fault
root.bind("<Destroy>", _destroy)




# Call animate() function periodically
#fargs = (ax1, ax2, xs, temps, lights, temp_c, lux)
fargs = (ax1, ax2, ax3, ax4, ax5, ax6, xs, temp1, temp2, temp3, Temp1GUI, Temp2GUI, Temp3GUI, pid1out, pid2out, pid3out, pid1GUI, pid2GUI, pid3GUI)
ani = animation.FuncAnimation(  fig, 
                                animate, 
                                fargs=fargs, 
                                interval=update_interval)               

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()
