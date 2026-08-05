#https://www.homeandlearn.uk/save-text-file-as.html

# this is my cool little data file handeler using tkinter file dialog boxes
# the idea is to have variables from process control program, that need to be saved and read from disk
# i have simply initiated the variables in this code for testing

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from time import strftime                                       # used to write data to disk


import os, sys

filename = ""
open_folder = "/home/pi/Documents/Python"

# Parameters
update_interval = 3000      # Time (ms) between polling/animation updates(read temps and update PID)
max_elements = 1440        # Maximum number of elements to store in plot lists
pwr_op_on = 10                    # PID power base line must get above to turn on
pwr_op_alm_limit = 100     # Max value PID ouput will get to before alarm shut down ( Heater not working)

# Initialise PID variables 
target1 = 27
P1 = 1
I1 = 1
D1= 11
interror1 = 0
error1 = 0
power1 = 0

target2 = 28
P2 = 1
I2 = 1
D2 = 22
interror2 = 0
error2 = 0
power2 = 0

target3 = 29
P3 = 1
I3 = 1
D3 = 33
interror3 = 0
error3 = 0
power3 = 0


#-------------------------------------------------------------------------------------------------
# open config file via dialog box. read file and pass to varaiables
def openfile():
    global filename
    global open_folder
    
    global update_interval      # Time (ms) between polling/animation updates(read temps and update PID)
    global max_elements        # Maximum number of elements to store in plot lists
    global pwr_op_on                    # PID power base line must get above to turn on
    global pwr_op_alm_limit     # Max value PID ouput will get to before alarm shut down ( Heater not working)

    global target1
    global P1
    global I1
    global D1

    global target2
    global P2
    global I2
    global D2

    global target3
    global P3
    global I3
    global D3

    filename =  filedialog.askopenfilename( initialdir = open_folder,
                                             title="Open A File" ,
                                             filetypes = ( ( "PP Extruder", "*.csv") , ("All files", "*.*") ) )
    try:
        if filename:
            the_file = open (filename, "r")   # open file for reading
            print ('Open File Name : ', filename)

            #must read file in here

            #data = the_file.read()           # read all characters from current position
            #data = the_file.read(20)           # read 20 characters from current position
            #position = the_file.tell()             #returns position pointer
            #position = the_file.seek (0, 0)    #seek(offset, whence_optional) offset= number of bytes to move
                                                                         # whence = 0, it means use the beginning of the file as the reference position
                                                                         # whence =  1 means use the current position as the reference position
                                                                         # whence =  2 then the end of the file would be taken as the reference position.

            #data = the_file.read()                  # display whole file
            #print (data)
            
            data = the_file.readline()              # read one line of data, see above options 
            print ('1 = ', (data))
                        
            data = the_file.readline()              # read one line of data, see above options 
            update_interval = float(data)
            print ('2 Update interval = ', update_interval)
                                  
            data = the_file.readline()              # read one line of data, see above options 
            max_elements =int(data)
            print ('3 max_elements = ', max_elements)

            data = the_file.readline()              # read one line of data, see above options 
            pwr_op_on  = int(data)
            print ('4 pwr_op_on  = ', pwr_op_on)
                                  
            data = the_file.readline()              # read one line of data, see above options 
            pwr_op_alm_limit  =int(data)
            print ('5 pwr_op_alm_limit  = ', pwr_op_alm_limit )

            data = the_file.readline()              # read one line of data, see above options 
            target1 = int(data)
            print ('6 target1  = ', target1)
                                  
            data = the_file.readline()              # read one line of data, see above options 
            P1 = int(data)
            print ('7 P1 = ', P1 )

            data = the_file.readline()              # read one line of data, see above options 
            I1 = int(data)
            print ('8 I1 = ', I1 )
                                  
            data = the_file.readline()              # read one line of data, see above options 
            D1 = int(data)
            print ('9 D1 = ', D1 )
                
            data = the_file.readline()              # read one line of data, see above options 
            target2 = int(data)
            print ('10 target2 = ', target2 )

            data = the_file.readline()              # read one line of data, see above options 
            P2 = int(data)
            print ('11 P2 = ', P2 )
                                  
            data = the_file.readline()              # read one line of data, see above options 
            I2 = int(data)
            print ('12 I2 = ', I2 )     
            
            data = the_file.readline()              # read one line of data, see above options 
            D2 = int(data)
            print ('13 D2 = ', D2 )     

            data = the_file.readline()              # read one line of data, see above options 
            target3 = int(data)
            print ('14 target3 = ', target3 )

            data = the_file.readline()              # read one line of data, see above options 
            P3 = int(data)
            print ('15 P3 = ', P3 )
                                  
            data = the_file.readline()              # read one line of data, see above options 
            I3 = int(data)
            print ('16 I3 = ', I3 )     
            
            data = the_file.readline()              # read one line of data, see above options 
            D3 = int(data)
            print ('17 D3 = ', D3 )     

            data = the_file.readline()              # read one line of data, see above options 
            open_folder = data
            print ('18 Open folder : ', open_folder )
            
            the_file.close()
            
        elif filename == ' ':
            messagebox.showinfo ( "Cancel", "you clicked Cancel")
    except IOError:
        messagebox.showinfo ( "Error", "could not open file")
        
#--------------------------------------------------------------------------------------------------------------------------------------------
# once a file is loaded it can be saved and updated
def savefile():
    global filename
    global open_folder
    
    global update_interval      # Time (ms) between polling/animation updates(read temps and update PID)
    global max_elements        # Maximum number of elements to store in plot lists
    global pwr_op_on                    # PID power base line must get above to turn on
    global pwr_op_alm_limit     # Max value PID ouput will get to before alarm shut down ( Heater not working)

    global target1
    global P1
    global I1
    global D1

    global target2
    global P2
    global I2
    global D2

    global target3
    global P3
    global I3
    global D3

    if filename:
        save_text = open(filename, 'w')
        print('Save File Name : ', filename )

        text_to_save = str("{0}\n".format(strftime("%d-%m-%y %H:%M:%S")))      #date and time, line 1(nice)
        save_text.write(text_to_save)
        text_to_save = (str(update_interval) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(max_elements) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(pwr_op_on) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(pwr_op_alm_limit) + "\n")
        save_text.write(text_to_save)

        text_to_save = (str(target1) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(P1) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(I1) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(D1) + "\n")
        save_text.write(text_to_save)

        text_to_save = (str(target2) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(P2) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(I2) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(D2) + "\n")
        save_text.write(text_to_save)

        text_to_save = (str(target3) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(P3) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(I3) + "\n")
        save_text.write(text_to_save)
        text_to_save = (str(D3) + "\n")
        save_text.write(text_to_save)
        text_to_save = (open_folder+"\n")       
        save_text.write(text_to_save)

        save_text.close()
    else:
        messagebox.showinfo ( "Error" , "No file open")
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# save file as
def savefileas():
    global filename
    global open_folder
    
    global update_interval      # Time (ms) between polling/animation updates(read temps and update PID)
    global max_elements        # Maximum number of elements to store in plot lists
    global pwr_op_on                    # PID power base line must get above to turn on
    global pwr_op_alm_limit     # Max value PID ouput will get to before alarm shut down ( Heater not working)

    global target1
    global P1
    global I1
    global D1

    global target2
    global P2
    global I2
    global D2

    global target3
    global P3
    global I3
    global D3

    save_text_as = filedialog.asksaveasfile(mode='w', defaultextension='.csv')
    filename = save_text_as.name          #set filename so we can do saves
    print ('Save As : ', filename)
    
    if save_text_as:                    #Do if True
        text_to_save = str("{0}\n".format(strftime("%d-%m-%y %H:%M:%S")))      #date and time, line 1(nice)
        save_text_as.write(text_to_save)
        text_to_save = (str(update_interval) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(max_elements) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(pwr_op_on) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(pwr_op_alm_limit) + "\n")
        save_text_as.write(text_to_save)

        text_to_save = (str(target1) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(P1) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(I1) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(D1) + "\n")
        save_text_as.write(text_to_save)

        text_to_save = (str(target2) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(P2) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(I2) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(D2) + "\n")
        save_text_as.write(text_to_save)

        text_to_save = (str(target3) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(P3) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(I3) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (str(D3) + "\n")
        save_text_as.write(text_to_save)
        text_to_save = (open_folder+"\n")       
        save_text_as.write(text_to_save)

        save_text_as.close()
    else:
        messagebox.showinfo("Error", "Cancelled")



# Create the main window
root = tk.Tk()
root.title("Zoe PID Controller")

#matchbox = os.popen('matchbox-keyboard')           #works
matchbox = os.popen('toggle-keyboard')                      #works only one key pad open closes others
#print (matchbox)
# Close opened file
#os.close( matchbox )


frame = tk.Frame(root)
frame.configure(bg='white')

dfont = 12

button_load_file = tk.Button(    frame, 
                            text="Load...", 
                            font=dfont,
                            command= openfile)
button_load_file.pack()

button_save_file = tk.Button(    frame, 
                            text="Save", 
                            font=dfont,
                            command= savefile)
button_save_file.pack()

button_save_file_as = tk.Button(    frame, 
                            text="Save As...", 
                            font=dfont,
                            command= savefileas)
button_save_file_as.pack()

entry_test = tk.Entry( frame, width = 30)
entry_test.pack()

frame.pack(fill=tk.BOTH, expand=1)
frame.pack()

#root = Tk()
#root.filename = filedialog.askopenfilename( initialdir = "/home/pi/Documents/Python",  title="Select A File" , filetypes = ( ( "how to files", "*.csv") , ("All files", "*.*") ) )
#print ( root.filename)

#testdata = ("{0},{1},{2}\n".format (str(target1),str(target2), str(target3)))
#print(testdata)

#with open("/home/pi/Documents/Python/Zoe_temps.csv", "a") as log:
 #       log.write("{0},{1},{2},{3}\n".format(strftime("%d-%m-%y %H:%M:%S"),str(temp1),str(temp2),str(temp3)))

