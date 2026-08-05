# Ths code does not work dont no why, it was working 

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

#---------------------------------------------------------------------------------------------
# clean up from any prvious tests
plt.close('all')

# Raspberry Pi:MAX6675 software SPI configuration.
CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

# Parameters
x_len = 200         # Number of points to display
y_range = [10, 40]  # Range of possible Y values to display

# Create Graph 1,figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('MAX6674 SPI Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (deg C)')

# Create Graph 2,figure for plotting
#fig2 = plt.figure('Graph 2')
#ax2 = fig2.add_subplot(1, 1, 1)
#xs1 = list(range(0, 200))
#yss = [0] * x_len
#ax2.set_ylim(y_range)

# Create a blank line. We will update the line in animate
#line2, = ax2.plot(xs1, ys2)

# Add labels
#plt.title('MAX6674 SPI  Temperature over Time')
#plt.xlabel('Samples')
#plt.ylabel('Temperature (deg C)')

#================================================================
#-------------- read 3 x SPI Temperature Sensors in Deg C -------------------
def tempdata():
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read MAX6675 tempuature Deg C
    [temp_c1, temp_c2, temp_c3] = tempdata()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
   
     # Add y to list
    ys.append(temp_c1)
    #yss.append(temp_c2)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    #yss = yss[-x_len:]

    # Update line with new Y values
    #plt.figure('Graph 1')
    line.set_ydata(ys)
    #plt.figure('Graph 2')
    #line2.set_ydata(ys2)

    return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ys), interval=600, blit=True)

plt.show()
