# 24-8-20 V2

# from tkinter import Tk
# from base import BaseWindow

# source info:-
# lawsie.github.io/guizero/about
# CMD: sudo pip3 install guizero
from guizero import App, Text, PushButton, TextBox

from gpiozero import CPUTemperature
from time import sleep, strftime, time

# CMD: sudo apt-get install python3-matplotlib
import matplotlib.pyplot as plt

# this works. use TkAgg backend might be default to this
#matplotlib.use("TkAgg")

#app=App()
#name=TextBox(app, text="Enter your name")
#app.display

#------------------
# INIT variables
#------------------


cpu = CPUTemperature()

plt.ion()
x=[]
y=[]


#================================================================
# Functions (subrotines)
#=============================

#start button
def start():
    start_button.disable()
    stop_button.enable()

#stop button
def stop():
    start_button.enable()
    stop_button.disable()

#write temp data to disk    
def write_temp(temp):
    text.value = int(text.value)+1
    
    with open("/home/pi/Documents/Python/cpu_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%y-%m-%d %H:%M:%S"),str(temp)))
        
#graph temp
def graph(temp):
        y.append(temp)
        x.append(time())
        plt.clf()
        plt.ylabel('Temperature DegC')
 #       plt.axis([
        plt.scatter(x,y)
        plt.plot(x,y)
        plt.draw()

#===========================================

temp = cpu.temperature        
app = App(title="hello world")
start_button = PushButton(app, command=start, text="start")
stop_button = PushButton(app, command=stop, text="stop", enabled=False)
text = Text(app, text="1")
text.repeat(1000, graph(temp))
app.display()


print ("hello")
#------------------------
# event loop
#-------------------
while True:
         temp = cpu.temperature
         write_temp(temp)
         graph(temp)         
         print (temp)
         print (time())
         
         plt.pause(1)
 

        


# close the open window before the prog moves on...wait....
        
                  



print ("hello")
