#ZoE: init_startup GUI
# this starts the GUI, draws screen is slow
"""
import tkinter as tk                     		# GUI function
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import messagebox

import tk_tools                                  # provids leds, and other GUI display elements

import matplotlib.figure as figure               # Animated graphs
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
"""
def init_GUI():    # Create the main window
    root = tk.Tk()
    root.title("Zoe PID Controller")

    # Create the main container
    frame = tk.Frame(root)
    frame.configure(bg='white')

    # Lay out the main container (expand to fit window)
    frame.pack(fill=tk.BOTH, expand=1)

    # Create figure for plotting
    fig = figure.Figure(figsize=(2, 2))
    fig.subplots_adjust(left=0.1, right=0.8)

       
    # Create 3 x Graphs
    ax1 = fig.add_subplot(3, 1, 1)
    ax3 = fig.add_subplot(3, 1, 2)
    ax5 = fig.add_subplot(3, 1, 3)

    # fig.tight_layout()                               #this works but very small graphs

    # Initiate a new set of axes that shares the same x-axis
    ax2 = ax1.twinx()
    ax4 = ax3.twinx()
    ax6 = ax5.twinx()

    # Empty x and y lists for storing data to plot later
    xs = []
    temp1 =[]
    temp2 = []
    temp3 = []
    pid1out =[]
    pid2out = []
    pid3out = []

    # Variables for holding temperature and PID data
    Temp1GUI =tk.DoubleVar()
    Temp2GUI = tk.DoubleVar()
    Temp3GUI = tk.DoubleVar()
    pid1GUI = tk.DoubleVar()
    pid2GUI = tk.DoubleVar()
    pid3GUI = tk.DoubleVar()

    # Create dynamic font for text
    dfont = tkFont.Font(size=-24)

    # load file Defaults.txt, on startup uses open_defaults_file = True to trigger, or not to
    openfile()

    # Create a Tk Canvas widget out of our figure
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_plot = canvas.get_tk_widget()

    # Define other supporting widgets (labels,  Input entry, buttons, LEDS )
    label_spacer1 = tk.Label(frame, text='   ', font=dfont, bg='white')
    label_spacer3 = tk.Label(frame, text='   ', font=dfont, bg='white')
    label_spacer4 = tk.Label(frame, text='   ', font=dfont, bg='white')

    label_line1 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')
    label_line2 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')
    label_line3 = tk.Label(frame, text='____________________________________________________________________', font=dfont, bg='white')

    label_file_name =tk.Label(frame, text='File Name: ', font=dfont, bg='white')

    label_temp1 = tk.Label(frame, text='Temp (Deg C):', font=dfont, bg='white')
    label_celsius1 = tk.Label(frame, textvariable=Temp1GUI, font=dfont, bg='white')
    label_target1 = tk.Label(frame, text='Target Temp 1: ', font=dfont, bg='white')
    label_power1 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
    label_powervalue1= tk.Label(frame, textvariable=pid1GUI, font=dfont, bg='white')
    label_P1 = tk.Label(frame, text='P: ', font=dfont, bg='white')
    label_I1 = tk.Label(frame, text='I: ' , font=dfont, bg='white')
    label_D1 = tk.Label(frame, text='D: ', font=dfont, bg='white')
    label_pidout1 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
    label_alarm1 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

    label_temp2 = tk.Label(frame, text='Temp (Deg C):', font=dfont, bg='white')
    label_celsius2 = tk.Label(frame, textvariable=Temp2GUI, font=dfont, bg='white')
    label_target2 = tk.Label(frame, text='Target Temp 2: ', font=dfont, bg='white')
    label_power2 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
    label_powervalue2= tk.Label(frame, textvariable=pid2GUI, font=dfont, bg='white')
    label_P2 = tk.Label(frame, text='P: ', font=dfont, bg='white')
    label_I2 = tk.Label(frame, text='I: ', font=dfont, bg='white')
    label_D2 = tk.Label(frame, text='D: ', font=dfont, bg='white')
    label_pidout2 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
    label_alarm2 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

    label_temp3 = tk.Label(frame, text='Temp (Deg C):', font=dfont, bg='white')
    label_celsius3 = tk.Label(frame, textvariable=Temp3GUI, font=dfont, bg='white')
    label_target3 = tk.Label(frame, text='Target Temp 3: ', font=dfont, bg='white')
    label_power3 = tk.Label(frame, text='Power Out: ', font=dfont, bg='white')
    label_powervalue3= tk.Label(frame, textvariable=pid3GUI, font=dfont, bg='white')
    label_P3 = tk.Label(frame, text='P: ', font=dfont, bg='white')
    label_I3 = tk.Label(frame, text='I: ', font=dfont, bg='white')
    label_D3 = tk.Label(frame, text='D: ', font=dfont, bg='white')
    label_pidout3 = tk.Label(frame, text='PID out: ', font=dfont, bg='white')
    label_alarm3 = tk.Label(frame, text='Alarm: ', font=dfont, bg='white')

    label_heater1= tk.Label(frame, text='Heater 1: ', font=dfont, bg='white')
    label_heater2= tk.Label(frame, text='Heater 2: ', font=dfont, bg='white')
    label_heater3= tk.Label(frame, text='Heater 3: ', font=dfont, bg='white')

    #---- 1
    sv = "StringVar()"
    entry_target1 = tk.Entry(frame, textvariable = sv, font=dfont, bg='white',  width=5)
    entry_target1.insert(0, target1)
    entry_target1.bind('<Key-Return>', on_target1_changed)
    entry_target1.bind('<FocusIn>',on_target1_focus)

    entry_P1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_P1.insert(0, P1)
    entry_P1.bind('<Key-Return>', on_P1_changed)

    entry_I1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_I1.insert(0, I1)
    entry_I1.bind('<Key-Return>', on_I1_changed)

    entry_D1 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_D1.insert(0, D1)
    entry_D1.bind('<Key-Return>', on_D1_changed)

    #------ 2
    entry_target2 = tk.Entry(frame, font=dfont, bg='white', width=5)
    entry_target2.insert(0, target2)
    entry_target2.bind('<Key-Return>', on_target2_changed)

    entry_P2 = tk.Entry(frame, font=dfont, bg='white', width=5)
    entry_P2.insert(0, P2)
    entry_P2.bind('<Key-Return>', on_P2_changed)

    entry_I2 = tk.Entry(frame, font=dfont, bg='white', width=5)
    entry_I2.insert(0, I2)
    entry_I2.bind('<Key-Return>', on_I2_changed)

    entry_D2 = tk.Entry(frame, font=dfont, bg='white', width=5)
    entry_D2.insert(0, D2)
    entry_D2.bind('<Key-Return>', on_D2_changed)

    #----- 3
    entry_target3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_target3.insert(0, target3)
    entry_target3.bind('<Key-Return>', on_target3_changed)

    entry_P3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_P3.insert(0, P3)
    entry_P3.bind('<Key-Return>', on_P3_changed)

    entry_I3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_I3.insert(0, I3)
    entry_I3.bind('<Key-Return>', on_I3_changed)

    entry_D3 = tk.Entry(frame, font=dfont, bg='white',  width=5)
    entry_D3.insert(0, D3)
    entry_D3.bind('<Key-Return>', on_D3_changed)


    entry_filename =tk.Entry(frame, font=dfont, bg='white',  width=45)
    entry_filename.insert(0, filename)
    entry_filename.bind('<Key-Return>', on_filename_changed)

    #-------------------------------------------------------------------------------
    button_load_file = tk.Button(    frame, 
                                text="Load...", 
                                font=dfont,
                                command= openfile)

    button_save_file = tk.Button(    frame, 
                                text="Save", 
                                font=dfont,
                                command= savefile)

    button_save_file_as = tk.Button(    frame, 
                                text="Save As...", 
                                font=dfont,
                                command= savefileas)

    button_config = tk.Button(    frame, 
                                text="Config...", 
                                font=dfont,
                                command= config)

    button_help = tk.Button(    frame,
                                text="Help",
                                font=dfont,
                                command=help_window)

    button_runpid1 = tk.Button(    frame, 
                                text="PID1 Run", 
                                font=dfont,
                                command=PID1_run)

    button_runpid2 = tk.Button(   frame,
                                text="PID2 Run",
                                font=dfont,
                                command=PID2_run)

    button_runpid3 = tk.Button(    frame,
                                text="PID3 Run",
                                font=dfont,
                                command=PID3_run)

    button_pid = tk.Button(   frame,
                                text="Toggle PID",
                                font=dfont,
                                command=toggle_Power)

    button_temp = tk.Button(    frame, 
                                text="Toggle Temp", 
                                font=dfont,
                                command=toggle_temp)

    button_manual = tk.Button(    frame, 
                                text="Manual Ctrl", 
                                font=dfont,
                                command=manual_ctrl)

    button_heater1 = tk.Button(   frame,
                                text="Pre-Heat 1",
                                font=dfont,
                                command=heater1)

    button_heater2 = tk.Button(    frame,
                                text="Pre-heat 2",
                                font=dfont,
                                command=heater2)

    button_heater3 = tk.Button(    frame,
                                text="Pre-heat 3",
                                font=dfont,
                                command=heater3)

    button_quit = tk.Button(    frame,
                                text="Quit",
                                font=dfont,
                                command=root.destroy)

    #led0 = tk_tools.Led(root, size=50, on_click_callback=on_click_callback)
    led_runpid1 = tk_tools.Led(frame, size=25)
    led_pidop1 = tk_tools.Led(frame, size=25)
    led_alarm1 = tk_tools.Led(frame, size=25)
    led_runpid1.to_green()
    led_pidop1.to_green()
    led_alarm1.to_red()

    led_runpid2 = tk_tools.Led(frame, size=25)
    led_pidop2 = tk_tools.Led(frame, size=25)
    led_alarm2 = tk_tools.Led(frame, size=25)
    led_runpid2.to_green()
    led_pidop2.to_green()
    led_alarm2.to_red()

    led_runpid3 = tk_tools.Led(frame, size=25)
    led_pidop3 = tk_tools.Led(frame, size=25)
    led_alarm3 = tk_tools.Led(frame, size=25)
    led_runpid3.to_green()
    led_pidop3.to_green()
    led_alarm3.to_red()

    led_manual =  tk_tools.Led(frame, size=25)
    led_heater1 = tk_tools.Led(frame, size=25)
    led_heater2 = tk_tools.Led(frame, size=25)
    led_heater3 = tk_tools.Led(frame, size=25)
    led_manual.to_red() 
    led_heater1.to_red()
    led_heater2.to_red()
    led_heater3.to_red()

    # The three geometry managers are: grid, pack, and place(pixel coordinents).
    # You should never mix geometry managers within the same hierarchy, but you can embed different
    # managers within each other (for example, you can lay out a frame widget with grid in a Toplevel and
    # then use pack to put different widgets within the frame).
    #
    # Lay out widgets in a grid in the frame. GRID is 11 colums (0-10) x 14 rows (0-13)
    #
    # this is the plot, starts at 0,0 spans 5 rows (down) and spans  5 colums (across)
    canvas_plot.grid(   row=0, 
                        column=0, 
                        rowspan=14, 
                        columnspan=5, 
                        sticky=tk.W+tk.E+tk.N+tk.S)

    # Poistion Widgets on grid
    #Example:-
    #label_temp1.grid(row=1, column=3, padx=100, pady=50, columnspan=2, sticky=tk.W)       

    # row 0 options
    #label_spacer1.grid(row = 0 , column = 0)

    label_file_name.grid(row =  0, column = 0)  
    entry_filename.grid(row=0, column = 1, columnspan=3)
        
    button_load_file.grid(row = 0 , column  = 5, sticky = tk.W)
    button_save_file.grid(row = 0, column = 6, sticky = tk.W)
    button_save_file_as.grid(row = 0, column = 7 )
    button_config.grid(row = 0, column = 8)
    button_help.grid (row = 0, column = 9)
    button_quit.grid(row=0, column=10, sticky = tk.E)

    #row 1 PID11
    label_target1.grid(row=1, column=5, sticky=tk.E)
    entry_target1.grid(row=1, column=6, sticky=tk.W)
    label_P1.grid(row=1, column=7, sticky=tk.E)
    entry_P1.grid(row=1, column=8, sticky=tk.W)
    button_runpid1.grid (row = 1, column = 9)
    led_runpid1.grid(row=1, column = 10)

    #row 2 PID1
    label_temp1.grid(row=2, column=5)
    label_celsius1.grid(row=2, column=6, sticky=tk.W)
    label_I1.grid(row=2, column=7, stick=tk.E)
    entry_I1.grid(row=2, column= 8, sticky =tk.W)
    label_pidout1.grid(row=2,  column = 9,sticky=tk.E)
    led_pidop1.grid(row=2, column = 10)

    #row 3 PID1
    label_D1.grid(row=3, column=7, sticky=tk.E)                
    entry_D1.grid(row=3, column=8, sticky=tk.W)
    label_heater1.grid(row=3, column =9, sticky = tk.E)
    led_heater1.grid(row=3, column = 10)

    #row 4 - PID1
    button_heater1.grid(row=4, column=5, sticky=tk.W)
    label_power1.grid(row=4, column=7, sticky=tk.E)
    label_powervalue1.grid(row=4, column=8, stick=tk.W)
    label_alarm1.grid(row=4, column=9, sticky=tk.E)
    led_alarm1.grid(row=4, column = 10)

    #row 5 - line
    label_line1.grid(row=5, column=5, columnspan=6, sticky=tk.W)

    #row 6 PID2
    label_target2.grid(row=6, column=5, sticky=tk.E)
    entry_target2.grid(row=6, column=6, sticky=tk.W)
    label_P2.grid(row=6, column=7, sticky=tk.E)
    entry_P2.grid(row=6, column=8, sticky=tk.W)
    button_runpid2.grid (row = 6, column = 9)
    led_runpid2.grid(row=6, column = 10)

    #row 7 PID 2
    label_temp2.grid(row=7, column=5)
    label_celsius2.grid(row=7, column=6, sticky=tk.W)
    label_I2.grid(row=7, column=7, sticky=tk.E)
    entry_I2.grid(row=7, column= 8, sticky=tk.W)
    label_pidout2.grid(row=7,  column = 9, sticky=tk.E)
    led_pidop2.grid(row=7, column = 10)

    #row 8 PID 2
    label_D2.grid(row=8, column=7, sticky=tk.E)                
    entry_D2.grid(row=8, column=8, sticky=tk.W)
    label_heater2.grid(row=8, column =9, sticky = tk.E)
    led_heater2.grid(row=8, column = 10)

    #row 9 PID 2
    button_heater2.grid(row=9, column=5, sticky=tk.W)
    label_power2.grid(row=9, column=7, sticky=tk.E)
    label_powervalue2.grid(row=9, column=8, sticky=tk.W)
    label_alarm2.grid(row=9, column=9,sticky=tk.E)
    led_alarm2.grid(row=9, column = 10)

    #row 10 - line
    label_line2.grid(row=10, column=5, columnspan=6, sticky=tk.W)

    #row 11 PID3
    label_target3.grid(row=11, column=5, sticky=tk.E)
    entry_target3.grid(row=11, column=6, sticky=tk.W)
    label_P3.grid(row=11, column=7, sticky=tk.E)
    entry_P3.grid(row=11, column=8, sticky=tk.W)
    button_runpid3.grid (row = 11, column = 9)
    led_runpid3.grid(row=11, column = 10)

    #row 12
    label_temp3.grid(row=12, column=5)
    label_celsius3.grid(row=12, column=6, sticky=tk.W)
    label_I3.grid(row=12, column=7,  sticky=tk.E)
    entry_I3.grid(row=12, column= 8,  sticky=tk.W)
    label_pidout3.grid(row=12,  column = 9, sticky=tk.E)
    led_pidop3.grid(row=12, column = 10)

    #row 13
    label_D3.grid(row=13, column=7, sticky=tk.E)                
    entry_D3.grid(row=13, column=8, sticky= tk.W)
    label_heater3.grid(row=13, column =9, sticky = tk.E)
    led_heater3.grid(row=13, column = 10)

    #row 14
    button_heater3.grid(row=14, column=5, sticky=tk.W)
    label_power3.grid(row=14, column=7, sticky=tk.E)
    label_powervalue3.grid(row=14, column=8, sticky=tk.W)
    label_alarm3.grid(row=14, column=9,sticky=tk.E)
    led_alarm3.grid(row=14, column = 10)

    #row 15 - bottom line
    button_pid.grid(row=15, column=0)
    button_temp.grid(row=15, column=1)
    button_manual.grid(row=15, column=2,sticky = tk.E)
    led_manual.grid(row=15, column = 3, sticky=tk.W)
    label_line3.grid(row=15, column=5, columnspan=6, sticky=tk.W)

    # row 16 - corner padding
    label_spacer3.grid(row = 16, column = 0)
    label_spacer4.grid(row = 16, column = 10)

    #----------------------------------------------------------------------------------------------
    # Add a standard 5 pixel padding to all widgets
    #for w in frame.winfo_children():
    #  w.grid(padx=5, pady=5)

    # Make it so that the grid cells expand out to fill window
    for i in range(0, 14):
        frame.rowconfigure(i, weight=1)
    for i in range(0, 10):
        frame.columnconfigure(i, weight=1)

