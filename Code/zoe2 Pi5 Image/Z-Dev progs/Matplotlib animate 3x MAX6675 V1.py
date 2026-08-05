# Graph real time temperature data from 3 x MAX6675, it works haha

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

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

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

xs = []
ys = []

xs2 = []
ys2 = []

xs3 = []
ys3 = []


# This function is called periodically from FuncAnimation
#def animate(i, xs, ys):
def animate(i, xs, ys, xs2, ys2, xs3, ys3):

    # Read MAX6675 tempuature Deg C
    temp_c1 = sensor1.readTempC()
    temp_c2 = sensor2.readTempC()
    temp_c3 = sensor3.readTempC()
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp_c1, temp_c2,temp_c3))
	
    
    # HANDY TIME FORMAT CHANGE HERE
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_c1)
    
    xs2.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys2.append(temp_c2)

    xs3.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys3.append(temp_c3)

    # Limit x and y lists to 30 items
    xs = xs[-30:]
    ys = ys[-30:]

    xs2 = xs2[-30:]
    ys2 = ys2[-30:]

    xs3 = xs3[-30:]
    ys3 = ys3[-30:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Temp_c1")
    ax.plot(xs2, ys2, label="Temp_c2")
    ax.plot(xs3, ys3, label="Temp_c3")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('3 x MAX6675 Thermocouples DegC over Time')
    plt.ylabel('Temperature (deg C)')
    plt.xlabel('Time (s)')
    plt.legend()  # Add a legend. But it bounces around with auto scaling

    

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, xs2, ys2, xs3, ys3),interval=1000)
plt.show()
