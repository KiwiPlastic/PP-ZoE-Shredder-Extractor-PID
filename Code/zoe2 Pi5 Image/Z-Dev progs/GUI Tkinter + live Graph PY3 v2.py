# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

# 24-8-20 v2
# Graphs one temp sensor live, but has Tkinter buttons etx, and hook in for PID loop
# has small issue of rubbish data at start of graph
# GOALS
# Adjust graph size
# trap code for PID
# more than one graph
#set up framwork to do what is required

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675

#---------------------------------------------------------------------------------------------
# clean up from any prvious tests, does not work now, but much more stable now
#plt.close('all')

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
x_len = 200                  # Number of points to display
y_range = [10, 40]      # Range of possible Y values to display

# --------------------- Graph setup --------------------------------------------------------------------
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(8,8), dpi=100)      #this size is the outside container 
#a = f.add_subplot(111)             # this does the same as ......
a = f.add_subplot(3,1,1)

xs = list(range(0, x_len))
ys = [0] * x_len
a.set_ylim(y_range)

# Create a blank line. We will update the line in animate
line, = a.plot(xs, ys)

# Add labels
a.set_title('TMP102 Temperature over Time')
a.set_xlabel('Samples')
a.set_ylabel('Temperature (deg C)')
#-------------------------------------------------------------------------------------------------------------

print(xs,ys)        #print the array for my ref

#============================================================

 #---------------------------------------------------------------------------------------------------------   
# this is the graphng code its activated at update_interval.
# Temperature is read here and the PID code could be updated here
#
def animate(i, ys):

    temp1 = sensor1.readTempC()     #read SPI temp value
    
    # Add y to list
    ys.append(temp1)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    #a.clear            #if used here will clear all preset labels and ranges. DONT USE
    a.plot(xs, ys)
    
    return line,

#----------------------------------------------------------------------------------------------------------------
# original code left in as example code

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
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

app = SeaofBTCapp()         #GUI tkinter code to setup pages. Event based, does not work if removed

#Update graph at poled interval, this should read temps and run PID code
ani = animation.FuncAnimation(f, animate, fargs=(ys,), interval=500, blit=True)
#ani = animation.FuncAnimation(f, animate2, interval=1000)

app.mainloop()      #this is the main loop, ie it focus is on the Tkinter window
        
