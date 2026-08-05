import tkinter as tk                                                  # GUI function
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure as figure

# Create the main window
root = tk.Tk()
root.title("Zoe PID Controller")

# Create the main container
frame = tk.Frame(root)
frame.configure(bg='white')

# Create figure for plotting
fig = figure.Figure(figsize=(2, 2))

# Create a Tk Canvas widget out of our figure
canvas = FigureCanvasTkAgg(fig, master=frame)


#----------------------------------
configwin = tk.Toplevel(root)
configwin.configure(bg='white')
    #configwin.geometry('950x900')          #let it self size, its a better result
configwin.title("Configuration Window")

intvar = tk.IntVar(configwin)

intvar.set(1)
print("Value of IntVar()", intvar.get()) 
checkbutton_pidautorun = tk.Checkbutton(configwin, variable=intvar, onvalue = 1, offvalue = 0, bg='white')

    #checkbutton_pidautorun.insert(0, intvar)
    #checkbutton_pidautorun.state(['selected']) 
    #chk.state(['!selected'])
    #checkbutton_pidautorun.set(1)
    #print ()
    #c = Checkbutton(master, text="Expand", variable=var)
    #c.pack()

checkbutton_pidautorun.grid(row=12, column=2, sticky=tk.W)


canvas.draw()
#----------------

root.mainloop()
