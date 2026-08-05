# Graph real time temperature data from MAX6675
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

plt.close('all')

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Raspberry Pi software SPI configuration. GPIO PINs
CLK = 14
CS  = 2
DO  = 15
sensor = MAX6675.MAX6675(CLK, CS, DO)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read MAX6675 tempuature Deg C
    temp_c = sensor.readTempC()
    print (temp_c)

    # Add x and y to lists
    # handy line to no this:-
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_c)

    # Limit x and y lists to 50 items
    xs = xs[-40:]
    ys = ys[-40:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('MAX6675 Temperature over Time')
    plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically, this is the key bit
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
