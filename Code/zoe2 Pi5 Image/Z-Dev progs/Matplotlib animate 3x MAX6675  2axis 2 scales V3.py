# Engine to Graph real time temperature data from 3 x MAX6675, it works haha
# 19-8-20 V3 changing to SUBPLOTS to get multi graphs - Done
# first examples where fine. However 3 graphs with two trace each and badly written code =  crash
# runs until array is full 30 Samples

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

#---------------------------------------------------------------------------------------------
# clean up from any prvious tests
plt.close('all')

#--------------------------------------------------------------------------------------------------
# only one of the following can be used, not both
# SUBPLOT, Create figure for plotting. this gives one graph with multi traces see V2 code or uncoment
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)

#SUBPLOTS, this gives mutli graphs in one figure. And Multi traces
fig2, ax1 = plt.subplots(3,1)       #3 graphs (axes), 1 figure

# Raspberry Pi:MAX6675 software SPI configuration.
CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

#------------------------------------------ Temp code until PID loop done ---------------------------------
# set initial PID out values
Output1 = input('Enter PID 1 output value: ')
if (Output1==""):
  Output1 = 20
Output1 = int(Output1)
#print ('Output1 = ', Output1)
#print ()

Output2 = input('Enter PID 2 output value: ')
if (Output2==""):
   Output2 = 40
Output2 = int(Output2)

Output3 = input ('Enter PID 3 output value: ')
if (Output3==""):
  Output3 = 80
Output3 = int(Output3)

#------------------------------------------------------------------------------------------------------------------------------

#config data plot arrays for graphs
xs = []                       # Time
ys = []                       # TempSensor 1
ys2 = []                    # TempSensor 2
ys3 = []                    # TempSensor 3
PID1Out = []            #PID 1 Output
PID2Out = []            #PID 2 Output
PID3Out = []            #PID 3 Output

#==================================================================
#----------------------------------------------------------------------------------------------
# SUBPLOT fuction.  we are not using it. Left as Example
#----------------------------------------------------------------------------------------------
# This function is called periodically from FuncAnimation
#def animate(i, xs, ys):
#def animate(i, xs, ys, xs2, ys2, xs3, ys3):
def animate(i, xs, ys, ys2, ys3):

    # Read MAX6675 tempuature Deg C
    [temp_c1, temp_c2, temp_c3] = tempdata()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
    
    # HANDY TIME FORMAT CHANGE HERE
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_c1)
    ys2.append(temp_c2)
    ys3.append(temp_c3)

    # Limit x and y lists to 30 items
    xs = xs[-30:]
    ys = ys[-30:]
    ys2 = ys2[-30:]
    ys3 = ys3[-30:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Temp_c1")
    ax.plot(xs, ys2, label="Temp_c2")
    ax.plot(xs, ys3, label="Temp_c3")

    # Format plot
    plt.xticks(ticks=range(1,30),rotation=45, ha='right')  # set to 30 as thats how many data points showing
    plt.subplots_adjust(bottom=0.30)
    plt.title('3 x MAX6675 Thermocouples DegC over Time')
    plt.ylabel('Temperature (deg C)')
    plt.xlabel('Time (s)')
    plt.legend()  # Add a legend. But it bounces around with auto scaling
    plt.ylim(10,40) # fix auto scale and set Temperature scale

        
#-------------- read 3 x SPI Temperature Sensors in Deg C -------------------
def tempdata():
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3

#============================================================
#--------------------------------------------------------------------------------------------------------------------    
# SUBPLOTS function. Draws 3 graphs with dif scales left/right
# This function is called periodically from FuncAnimation
def animate2(i, xs, ys, ys2, ys3, PID1Out, PID2Out, PID3Out, Output1, Output2, Output3):

#May need a Fuction call here to update these values??? 
    PID1 = Output1
    PID2 = Output2
    PID3 = Output3

    # Read MAX6675 tempuature Deg C
    [temp_c1, temp_c2, temp_c3] = tempdata()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
    print ()
    print (ys)
    
    # HANDY TIME FORMAT CHANGE HERE
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    
    # Add x and y to array lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_c1)
    ys2.append(temp_c2)
    ys3.append(temp_c3)
    PID1Out.append(PID1)
    PID2Out.append(PID2)
    PID3Out.append(PID3)

    # Limit x and y array lists to 30 items
    xs = xs[-10:]
    ys = ys[-10:]
    ys2 = ys2[-10:]
    ys3 = ys3[-10:]
    PID1Out = PID1Out[-10:]
    PID2Out = PID2Out[-10:]
    PID2Out = PID2Out[-10:]

    #-----------First Graph Temperature 1 & PID1 output ----------------------------------------
    color = 'tab:red'
    ax1[0].set_xlabel('time (s)')
    ax1[0].set_ylabel('Temp1 DegC', color=color)
    ax1[0].plot(xs, ys, color=color)
    ax1[0].tick_params(axis='y', labelcolor=color)
    ax1[0].set_ylim(10,40)
    
    ax2 = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('PID1 Out', color=color)  # we already handled the x-label with ax1
    ax2.plot(xs, PID1Out, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(10,100)

    #-----------2nd Graph Temperature 2 & PID2 output ----------------------------------------
    color = 'tab:red'
    ax1[1].set_xlabel('time (s)')
    ax1[1].set_ylabel('Temp2 DegC', color=color)
    ax1[1].plot(xs, ys2, color=color)
    ax1[1].tick_params(axis='y', labelcolor=color)
    ax1[1].set_ylim(10,40)
    
    ax3 = ax1[1].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax3.set_ylabel('PID2 Out', color=color)  # we already handled the x-label with ax1
    ax3.plot(xs, PID2Out, color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.set_ylim(10,100)

    #-----------3nd Graph Temperature 3 & PID3 output ----------------------------------------
    color = 'tab:red'
    ax1[2].set_xlabel('time (s)')
    ax1[2].set_ylabel('Temp3 DegC', color=color)
    ax1[2].plot(xs, ys3, color=color)
    ax1[2].tick_params(axis='y', labelcolor=color)
    ax1[2].set_ylim(10,40)
    
    ax4 = ax1[2].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax4.set_ylabel('PID3 Out', color=color)  # we already handled the x-label with ax1
    ax4.plot(xs, PID3Out, color=color)
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.set_ylim(10,100)
    
    fig2.tight_layout()  # otherwise the right y-label is slightly clipped
    #plt.show()

''' EXAMPLE STUFF from SUBPLOT

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Temp_c1")
    ax.plot(xs, ys2, label="Temp_c2")
    ax.plot(xs, ys3, label="Temp_c3")

    # Format plot
    plt.xticks(ticks=range(1,30),rotation=45, ha='right')  # set to 30 as thats how many data points showing
    plt.subplots_adjust(bottom=0.30)
    plt.title('3 x MAX6675 Thermocouples DegC over Time')
    plt.ylabel('Temperature (deg C)')
    plt.xlabel('Time (s)')
    plt.legend()  # Add a legend. But it bounces around with auto scaling
    plt.ylim(10,40) # fix auto scale and set Temperature scale

  '''      
#==========================================================================    

# Set up plot to call animate() function periodically(interval=1000).
# this is Object Orientated code??
# 7 arrays, of 30 data points each. 3 x PID output values witch are added to the array inside
# the function animate2.
# this fuction/object just happens. Hopefull the PID out value will update
ani = animation.FuncAnimation(fig2, animate2, fargs=(xs, ys, ys2, ys3, PID1Out, PID2Out, PID3Out, Output1, Output2, Output3),interval=1000)

#------------------------------------------------------------------------------

# get Temperature Readings from function tempdata()
[Temp1, Temp2, Temp3] = tempdata()


plt.show()
