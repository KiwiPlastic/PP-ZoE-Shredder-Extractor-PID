# First play, guizero not working, so comment out and move on
#..and then it worked. Think cos do file association *.py => Python3

# from tkinter import Tk
# from base import BaseWindow

# lawsie.github.io/guizero/about
# CMD: sudo pip3 install guizero
from guizero import App, Text, PushButton, TextBox

#app=App()
#name=TextBox(app, text="Enter your name")
#app.display




def start():
    start_button.disable()
    stop_button.enable()

def stop():
    start_button.enable()
    stop_button.disable()
    
app = App(title="hello world")
start_button = PushButton(app, command=start, text="start")
stop_button = PushButton(app, command=stop, text="stop", enabled=False)

app.display()

# close the open window before the prog moves on...wait....


#------------------
# INIT
#------------------

from gpiozero import CPUTemperature
from time import sleep, strftime, time


# CMD: sudo apt-get install python3-matplotlib
import matplotlib.pyplot as plt

cpu = CPUTemperature()

plt.ion()
x=[]
y=[]


#---------------
# subrotines
#--------------------

def write_temp(temp):
    
    with open("/home/pi/Documents/Python/cpu_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%y-%m-%d %H:%M:%S"),str(temp)))
        
                  
def graph(temp):
        y.append(temp)
        x.append(time())
        plt.clf()
        plt.ylabel('Temperature DegC')
 #       plt.axis([
        plt.scatter(x,y)
        plt.plot(x,y)
        plt.draw()
        
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
 

        
        
                  



print ("hello")
