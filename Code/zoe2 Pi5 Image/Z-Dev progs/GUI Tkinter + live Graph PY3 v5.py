# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

# 24-8-20 V5
# Based on Bliting 9.py and GUI Tkinter + Graph PY2 base code
# 
# Graphs 3 temp sensor live, but has Tkinter buttons etx, and hook in for PID loop
# has small issue of rubbish data at start of graph. but very stable
#
#GOALS
# tidy up graphs - Tight fit - DONE V4
# remaned to: GUI Tkinter + live Graph PY3 v5.py
# Adjust graph size, inside figure, see 'Gui Tkinter and Matplotlib PY3.py'
#
# this is the start......
#
# add code for PID
# add two traces per graph, dif scales
# 
# Screen GUI layout to do what is required, buttons and iputs, setting display

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

#from tkinter import *                   #import all classes/methods from the tkinter module
import tkinter as tk
from tkinter import ttk

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

#---------------------------------------------------------------------------------------------

#====================================================
#               INIT Global VARIABLES 
#====================================================

# GPIO pin asignment, using GPIO labeling, not pin header
CLK = 14
CS1 = 2
CS2 = 3
CS3 = 4
DO  = 15

#HEATER1 =
#HEATER2 =
#HEATER3 =

# SPI MAX6675 software configuration (temperature Sensors)
sensor1 = MAX6675.MAX6675(CLK, CS1, DO)
sensor2 = MAX6675.MAX6675(CLK, CS2, DO)
sensor3 = MAX6675.MAX6675(CLK, CS3, DO)

# Init Parameters
x_len = 200                  # Number of points to display,graph time scale
y_range = [10, 40]      # Range of possible Y values to display, temperature range
sample_Int = 1000    #Graph update sample interval in ms 1000 = 1 Sec

# --------------------- Graph setup --------------------------------------------------------------------
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(8,8), dpi=100)      #this size is the outside container of the graph
a1 = f.add_subplot(3,1,1)
a2 = f.add_subplot(3,1,2)
a3 = f.add_subplot(3,1,3)

xs1 = list(range(0, x_len))

ys1 = [0] * x_len
a1.set_ylim(y_range)

ys2 = [0] * x_len
a2.set_ylim(y_range)

ys3 = [0] * x_len
a3.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line1, = a1.plot(xs1, ys1)
line2, = a2.plot(xs1, ys2)
line3, = a3.plot(xs1, ys3)

# Add labels
a1.set_title('Temperature  1 over Time')
a1.set_xlabel('Samples')
a1.set_ylabel('Temperature (deg C)')

a2.set_title('Temperature  2 over Time')
a2.set_xlabel('Samples')
a2.set_ylabel('Temperature (deg C)')

a3.set_title('Temperature  3 over Time')
a3.set_xlabel('Samples')
a3.set_ylabel('Temperature (deg C)')

f.tight_layout()        # this makes the labels fit, haha how cool was that one

#-------------------------------------------------------------------------------------------------------------

print(xs1,ys1)        #print the array for my ref

#============================================================

 #---------------------------------------------------------------------------------------------------------   
# this is the graphng code its activated at update_interval.
# 3 xTemperature is read here and the PID code could be updated here
#
def animate(i, ys1, ys2, ys3):

    temp1 = sensor1.readTempC()     #read SPI temp value
    temp2 = sensor2.readTempC()     #read SPI temp value
    temp3 = sensor3.readTempC()     #read SPI temp value
    print ('Thermocouple Temperature: {0:0.2F}°C   {1:0.2F} C   {2:0.2F} C'.format(temp1, temp2,temp3))
    
   #Could do PID loop Here 
    
    # Add temps y to lists
    ys1.append(temp1)
    ys2.append(temp2)
    ys3.append(temp3)
      
    # Limit y list to set number of items
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]
    ys3 = ys3[-x_len:]

    # Update line with new Y values
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)
    line3.set_ydata(ys3)

    a1.plot(xs1, ys1)
    a2.plot(xs1, ys2)
    a3.plot(xs1, ys3)
    
    return line1, line2, line3

#----------------------------------------------------------------------------------------------------------------
# original code left in as example code: reading data from a file to graph

def animate2(i):
    pullData = open("sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

#-----------------------------------------------------------------------------------------------------------------------------    
# Main GUI page display switching interface, event based             
#
class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ZoE Master Control Center V5")
        
        container = tk.Frame(self)
        #container = Tk.Frame(self)                 # from other code
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        window = tk.Tk()
        #container.geometry("1000x1000") 
        window.geometry("1000x1000") 

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        label = tk.Label(self, text="Rich test. this is a packer!", font=LARGE_FONT)
        label.pack(pady=20, padx=20)

        #update graph
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#===================================================================

#app = SeaofBTCapp()         #GUI tkinter code to setup pages. Event based, does not work if removed

'''
#-----------------------------------------------------
# the main Tkinter window 
window = Tk() 

# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("1000x1000") 



# button that displays the plot 
plot_button = Button(master = window,  command = plot, height = 2, width = 10, text = "Plot") 

# place the button 
# in main window 
plot_button.pack() 

  #update graph
canvas = FigureCanvasTkAgg(f, self)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, self)
toolbar.update()
        
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# run the gui 
window.mainloop() 
'''
app = SeaofBTCapp()         #GUI tkinter code to setup pages. Event based, does not work if removed

#Update graph at poled interval, this reads temps and runs PID code
ani = animation.FuncAnimation(f, animate, fargs=(ys1, ys2, ys3), interval=sample_Int, blit=True)
#ani = animation.FuncAnimation(f, animate2, interval=1000)

app.mainloop()      #this is the main loop, ie it focus is on the Tkinter window




