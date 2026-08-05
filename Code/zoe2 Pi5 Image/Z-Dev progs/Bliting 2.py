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

# Create figure for plotting FIGURE 1---------------------------
#fig = plt.figure(1)
f1 = plt.figure(1)
ax = f1.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('TMP102 Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (deg C)')

# -----------------------------------------FIGURE 2 ------------------------------
f2 = plt.figure(2)
axb = f2.add_subplot(1, 1, 1)
xsb = list(range(0, 200))
ysb = [0] * x_len
axb.set_ylim(y_range)

# Create a blank line. We will update the line in animate
lineb, = axb.plot(xsb, ysb)

# Add labels
plt.title('TMP102 Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (deg C)')

#------------------------------------------------------------------------------------------

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read MAX6675 tempuature Deg C
    [temp_c1, temp_c2, temp_c3] = tempdata()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
    
    # Add y to list
    ys.append(temp_c1)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    plt.figure(1)

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

#-------------- read 3 x SPI Temperature Sensors in Deg C -------------------
def tempdata():
    temp1 = sensor1.readTempC()
    temp2 = sensor2.readTempC()
    temp3 = sensor3.readTempC()
    return temp1, temp2, temp3

#-------------------------------------------------------------------------------------------------------
# This function is called periodically from FuncAnimation
def animate2(i, ys):

    # Read MAX6675 tempuature Deg C
    [temp_c1, temp_c2, temp_c3] = tempdata()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
    
    # Add y to list
    ys.append(temp_c1)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    plt.figure(1)

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

#============================================================



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(f1,
    animate,
    fargs=(ys,),
    interval=600,
    blit=True)
plt.show()
