# Zoe: provides initial values and file operations
# comes to def init() at startup

from time import strftime           # used to write data to disk??

import Zoe_CLI

#====================================================
#               INIT Global VARIABLES 
#====================================================
    
# Initialise PID variables
target1 = 40
P1 = 0.9
I1 = 0.01
D1 = 0.001
interror1 = 0.0
error1 = 0.0
power1 = 0.0
PID1_run_state = False
heater1_state = False
PID1_alarm_state = False

target2 = 41
P2 = 0.1
I2 = 0.1
D2 = 0.0
interror2 = 0
error2 = 0
power2 = 0
PID2_run_state = False
heater2_state = False
PID2_alarm_state = False

target3 = 42
P3 = 0.1
I3 = 0.1
D3 = 0.0
interror3 = 0
error3 = 0
power3 = 0
PID3_run_state = False
heater3_state = False
PID3_alarm_state = False

pizo_state = False

# file handeling tags
open_folder = "/home/richn/zoe2/Data"
filename = (open_folder+"/Defaults.txt")

#=========================================
def init():
    print ("hello...Starting...")
    
    global target1
    global P1
    global I1
    global D1
    global interror1
    global error1
    global power1
    global PID1_run_state
    global heater1_state
    global PID1_alarm_state 
   
    global target2
    global P2
    global I2
    global D2
    global interror2
    global error2
    global power2
    global PID2_run_state
    global heater2_state
    global PID2_alarm_state
    
    global target3
    global P3
    global I3
    global D3
    global interror3
    global error3
    global power3
    global PID3_run_state
    global heater3_state
    global PID3_alarm_state
    
    global pizo_state
    
#====================================
def openfile():						# open config file via dialog box. Read file and pass to varaiables
    
    global filename
    
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
                
        the_file = open (filename, "r")                 # open file for reading
        print ('Open File Name : ', filename)

        data = the_file.readline()                      # Date & time saved last (not used)
        print ('Last updated = ', (data))
                    
        data = the_file.readline()                      # read one line of data         target1
        Zoe_CLI.target1 = float(data)
        print ('target1  = ', Zoe_CLI.target1)
        
        data = the_file.readline()                      # read one line of data         P1
        Zoe_CLI.P1 = float(data)
        print ('P1 = ', Zoe_CLI.P1 )

        data = the_file.readline()                      # read one line of data         I1
        Zoe_CLI.I1 = float(data)
        print ('I1 = ', Zoe_CLI.I1 )
                              
        data = the_file.readline()                      # read one line of data         D1
        Zoe_CLI.D1 = float(data)
        print ('D1 = ', Zoe_CLI.D1 )
            
        data = the_file.readline()                      # read one line of data         target2
        Zoe_CLI.target2 = float(data)
        print ('target2 = ', Zoe_CLI.target2 )

        data = the_file.readline()                      # read one line of data         P2
        Zoe_CLI.P2 = float(data)
        print ('P2 = ', Zoe_CLI.P2 )
                              
        data = the_file.readline()                      # read one line of data         I2
        Zoe_CLI.I2 = float(data)
        print ('I2 = ', Zoe_CLI.I2 )     
        
        data = the_file.readline()                      # read one line of data         D2
        Zoe_CLI.D2 = float(data)
        print ('D2 = ', Zoe_CLI.D2 )     

        data = the_file.readline()                      # read one line of data         target3
        Zoe_CLI.target3 = float(data)
        print ('target3 = ', Zoe_CLI.target3 )

        data = the_file.readline()                      # read one line of data         P3
        Zoe_CLI.P3 = float(data)
        print ('P3 = ', Zoe_CLI.P3 )
                              
        data = the_file.readline()                      # read one line of data         I3
        Zoe_CLI.I3 = float(data)
        print ('I3 = ', Zoe_CLI.I3 )     
        
        data = the_file.readline()                      # read one line of data         D3
        Zoe_CLI.D3 = float(data)
        print ('D3 = ', D3 )

        data = the_file.readline()                      # read one line of data         open_folder
        open_folder = data
        print ('Opened folder : ', open_folder )

        the_file.close()                                # close file ......

# ===================================
def savefile():											# Save config
    
    global filename
    
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
    
    target1 = Zoe_CLI.target1
    P1 = Zoe_CLI.P1
    I1 = Zoe_CLI.I1
    D1 = Zoe_CLI.D1
    
    target2 = Zoe_CLI.target2
    P2 = Zoe_CLI.P2
    I2 = Zoe_CLI.I2
    D2 = Zoe_CLI.D2
    
    target3 = Zoe_CLI.target3
    P3 = Zoe_CLI.P3
    I3 = Zoe_CLI.I3
    D3 = Zoe_CLI.D3
    
    if filename:
        save_text = open(filename, 'w')
        print('Save File Name : ', filename )

        text_to_save = str("{0}\n".format(strftime("%d-%m-%y %H:%M:%S")))      #date and time, line 1(nice)
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
        
        text_to_save = (open_folder) 			#save file path Zoe for ref      
        save_text.write(text_to_save)
        
        save_text.close()

