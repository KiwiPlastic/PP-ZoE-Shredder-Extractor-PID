# 20-8-20 Bliting code Ver 6
# shows 3 graphs (x_len=) 200 samples wide, reads 3 x MAX6675 SPIs
# untill this version, it normaly had memory leaks in matplotlib
# graphs are objects that are updated on an event call set up before the main Event loop
# Event loop not developed in this version, but started on
# 
# small improvements
# - separate Temp data readings, one call per sesnor per graph - DONE
# - can all animate function calls be on same interval - YES DONE
# - x_len hooked into xs - Changeing the value, was crashing. DONE,  TESTED  OK. 
# - use numbers on labels: xs3, xs2 a b c labels confusing - DONE
# - add graph sample interval presetable value - DONE
# - get a while loop working to test it (print temps) - DONE V6
# - graph figure size and position to stop overlaying. Makes for flicker - DONE V7
# - Re test reading variables from a function
# - PID code
# - write to disk
# - next version will look at a second line on each graph

#-------------------------------------------------------------------------------------------
from time import sleep, strftime, time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

#---------------------------------------------------------------------------------------------
# clean up from any prvious program test runs, else memory leak.
plt.close('all')

#------------------------------ INIT -------------------------------------------------------

# Raspberry Pi: MAX6675 software SPI configuration.
CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

# Init Parameters
x_len = 200                  # Number of points to display
y_range = [10, 40]      # Range of possible Y values to display
sample_Int = 1000    #Graph update sample interval in ms 1000 = 1 Sec
test1 = 0                       #

# --------------------------------------- Init Graph Figures Sizes ------------------------------------
print (plt.rcParams.get('figure.figsize'))      #print curent value of figure size 
# default size is 6.4 x 4.8

#fig = plt.figure(figsize=(6,8))        # this does not work, it also does not produce error

# set up new Figure Size
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 6
fig_size[1] = 4.8
plt.rcParams["figure.figsize"] = fig_size

backend = matplotlib.get_backend()
print ('Backend = ', backend)
print ()
print('Fig size = ', plt.rcParams.get("figure.figsize" ))

# ----------------------------------- FIGURE 1 Create figure for plotting ---------------------------
f1 = plt.figure(1)                                  # this line sets the focus to fig 1, then build the graph frame work
ax1 = f1.add_subplot(1, 1, 1)

x = 10
y = 35
f1.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))     #set the absolute position the Figure on screen

xs1 = list(range(0, x_len))
ys1 = [0] * x_len
ax1.set_ylim(y_range)           #set Y axis limit

line1, = ax1.plot(xs1, ys1)     # Create a blank line. We will update the line in animate

# Add labels
plt.title('MAX6675 Thermocouple Temperature 1')
plt.xlabel('Samples')
plt.ylabel('Temperature 1 (deg C)')

# -----------------------------------------FIGURE 2 ------------------------------
f2 = plt.figure(2)
ax2 = f2.add_subplot(1, 1, 1)

x = 612
Y = 35
f2.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))     #set the absolute fig pos on screen

xs2 = list(range(0, x_len))
ys2 = [0] * x_len
ax2.set_ylim(y_range)       #set Y axis limit

line2, = ax2.plot(xs2, ys2)     # Create a blank line. We will update the line in animate

# Add labels
plt.title('MAX6675 Thermocouple Temperature 2')
plt.xlabel('Samples')
plt.ylabel('Temperature 2 (deg C)')

# -----------------------------------------FIGURE 3 ------------------------------
f3 = plt.figure(3)
ax3 = f3.add_subplot(1, 1, 1)

x = 1214
Y = 35
f3.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))     #set the absolute fig pos on screen

xs3 = list(range(0, x_len))
ys3 = [0] * x_len
ax3.set_ylim(y_range)           #set Y axis limit

line3, = ax3.plot(xs3, ys3)     # Create a blank line. We will update the line in animate

# Add labels
plt.title('MAX6675 Thermocouple Temperature 3')
plt.xlabel('Samples')
plt.ylabel('Temperature 3 (deg C)')

#-------------- read 3 x SPI Temperature Sensors in Deg C -------------------
def tempdata():
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3

# these 3 wont work, with out the other values could be an indexing thing, so preload with =0
# doing this to speed up the code run time ie not reading 3 x SPI each time
# be better to read 3 x spi then setup graph for three.
#Instead we read each SPI then read again in While loop, coursing exsesive runtime
#...but this code works (Inefechent can be reliable)
#
#-------------- read Temp 1  SPI Temperature Sensors in Deg C -------------------
def tempdata_1():
    temp1 = sensor1.readTempC()
    temp2 = 0
    temp3 = 0
    return temp1, temp2, temp3

#-------------- read Temp 2  SPI Temperature Sensors in Deg C -------------------
def tempdata_2():
    temp1 = 0
    temp2 = sensor2.readTempC()
    temp3 = 0
    return temp1, temp2, temp3

#-------------- read Temp 3  SPI Temperature Sensors in Deg C -------------------
def tempdata_3():
    temp1 = 0
    temp2 = 0
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3

#------------------------------------------------------------------------------------------
# Update Graph 1.  This function is called periodically from FuncAnimation. 
def animate_1(i, ys1):

    # Get Temp 1 - Read MAX6675 tempuature Deg C
    #[temp_c1, temp_c2, temp_c3] = tempdata_1()
    temp_c1 = sensor1.readTempC()

    # Add y to list
    ys1.append(temp_c1)

    # Limit y list to set number of items
    ys1 = ys1[-x_len:]

    # set focus to fig1 (Graph 1)
    plt.figure(1)

    # Update line with new Y values
    line1.set_ydata(ys1)
    
    return line1, 

#-------------------------------------------------------------------------------------------------------
# Update Graph 2. This function is called periodically from FuncAnimation. 
def animate_2(i, ys2):

    # Get Temp 2 - Read MAX6675 tempuature Deg C
    #[temp_c1, temp_c2, temp_c3] = tempdata_2()
    temp_c2 = sensor2.readTempC()
        
    # Add y to list
    ys2.append(temp_c2)

    # Limit y list to set number of items
    ys2 = ys2[-x_len:]

    # set focus to fig2 (Graph 2 )
    plt.figure(2)

    # Update line with new Y values
    line2.set_ydata(ys2)

    return line2,

#-------------------------------------------------------------------------------------------------------
# Update Graph 3. This function is called periodically from FuncAnimation. 
def animate_3(i, ys3):

    # Get Temp 3 - Read MAX6675 tempuature Deg C
    #[temp_c1, temp_c2, temp_c3] = tempdata_3()
    #temp_c1 = sensor1.readTempC()
    temp_c3 = temp3
    # Add y to list
    ys3.append(temp_c3)

    # Limit y list to set number of items
    ys3 = ys3[-x_len:]

    # set focus to fig3 (Graph3)
    plt.figure(3)

    # Update line with new Y values
    line3.set_ydata(ys3)

    return line3,
#============================================================


#Update Graph 1 and update at interval = smaple-Int (set at start of prog_init)
ani1 = animation.FuncAnimation(f1,
        animate_1,
        fargs=(ys1,),
        interval=sample_Int,
        blit=True)

#Update Graph 2
ani2 = animation.FuncAnimation(f2,
        animate_2,
        fargs=(ys2,),
        interval=sample_Int,
        blit=True)

#Update Graph 3
ani3 = animation.FuncAnimation(f3,
        animate_3,
        fargs=(ys3,),
        interval=sample_Int,
        blit=True)

# to get control
#----uncoment this one
#plt.show()
#---""" this following part......


#=====================================
#    event loop
#=====================================
while True:

    #[temp_c1, temp_c2, temp_c3] = tempdata()
    [temp1, temp2, temp3] = tempdata()
    #print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp1, temp2,temp3))
    test1 = test1+1
    plt.pause(0.1)    # this line is required else graphs wont work
    sleep(0.2)

    
