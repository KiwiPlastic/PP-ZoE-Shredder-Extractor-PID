# Command Line Interface Processing
#
# command's
# q 		Quit
# ? 		Help
# s         Save settings
# d			Load Defaults (reset)
# k 		Kill - Shutdown Pizo, Heaters, and PIDs OFF
# p 		Pizo On/Off Toggel		
#
# r1 		PID 1 Run On/Off Toggel
# t1=nn.n 	PID 1 Target Deg
# p1=n.n	PID 1 P
# i1=n.n	PID 1 I
# d1=n.n	PID 1 D
# ...
#
# h1		Heater 1 On/Off Toggel
# h2		Heater 2 On/Off Toggel
# h3		Heater 3 On/Off Toggel
#
#=======================================================

import os, sys
import select						# keyboard input for CLI (non blocking)

import Zoe_Outputs
import Zoe_ConfigFile
import Zoe_Help_text

target1 = Zoe_ConfigFile.target1
P1 = Zoe_ConfigFile.P1
I1 = Zoe_ConfigFile.I1
D1 = Zoe_ConfigFile.D1
PID1_run_state = Zoe_ConfigFile.PID1_run_state
heater1_state = Zoe_ConfigFile.heater1_state

target2 = Zoe_ConfigFile.target2
P2 = Zoe_ConfigFile.P2
I2 = Zoe_ConfigFile.I2
D2 = Zoe_ConfigFile.D2
PID2_run_state = Zoe_ConfigFile.PID2_run_state
heater2_state = Zoe_ConfigFile.heater2_state

target3 = Zoe_ConfigFile.target3
P3 = Zoe_ConfigFile.P3
I3 = Zoe_ConfigFile.I3
D3 = Zoe_ConfigFile.D3
PID3_run_state = Zoe_ConfigFile.PID3_run_state
heater3_state = Zoe_ConfigFile.heater3_state

pizo_state = Zoe_ConfigFile.pizo_state

PID_GainChangeFlag = False 

#============================================
def init():
    print ("init default settings")
    global target1
    global P1
    global I1
    global D1
    global interror1
    global error1
    global power1
    global PID1_run_state
    global heater1_state
    
    global target2
    global P2
    global I2
    global D2
    global interror2
    global error2
    global power2
    global PID2_run_state
    global heater2_state
    
    global target3
    global P3
    global I3
    global D3
    global interror3
    global error3
    global power3
    global PID3_run_state
    global heater3_state
    
    global pizo_state
    
    global PID_GainChangeFlag
    
    target1 = Zoe_ConfigFile.target1
    P1 = Zoe_ConfigFile.P1
    I1 = Zoe_ConfigFile.I1
    D1 = Zoe_ConfigFile.D1
    interror1 = Zoe_ConfigFile.interror1
    error1 = Zoe_ConfigFile.error1
    power1 = Zoe_ConfigFile.power1
    PID1_run_state = Zoe_ConfigFile.PID1_run_state
    heater1_state = Zoe_ConfigFile.heater1_state

    target2 = Zoe_ConfigFile.target2
    P2 = Zoe_ConfigFile.P2
    I2 = Zoe_ConfigFile.I2
    D2 = Zoe_ConfigFile.D2
    interror2 = Zoe_ConfigFile.interror2
    error2 = Zoe_ConfigFile.error2
    power2 = Zoe_ConfigFile.power2
    PID2_run_state = Zoe_ConfigFile.PID2_run_state
    heater2_state = Zoe_ConfigFile.heater2_state

    target3 = Zoe_ConfigFile.target3
    P3 = Zoe_ConfigFile.P3
    I3 = Zoe_ConfigFile.I3
    D3 = Zoe_ConfigFile.D3
    interror3 = Zoe_ConfigFile.interror3 
    error3 = Zoe_ConfigFile.error3
    power3 = Zoe_ConfigFile.power3
    PID3_run_state = Zoe_ConfigFile.PID3_run_state
    heater3_state = Zoe_ConfigFile.heater3_state

    pizo_state = Zoe_ConfigFile.pizo_state
    
    PID_GainChangeFlag = False
    
#=======================================================
#def cmd(PID1_run_state=False, PID2_run_state=False, PID3_run_state=False, heater1_state=False, heater2_state=False, heater3_state=False, pizo_state=False):
def cmd():
    global target1
    global P1
    global I1
    global D1
    global PID1_run_state
    global heater1_state
    
    global target2
    global P2
    global I2
    global D2
    global PID2_run_state
    global heater2_state
    
    global target3
    global P3
    global I3
    global D3
    global PID3_run_state
    global heater3_state
    
    global pizo_state
    
    global PID_GainChangeFlag
    
    input = select.select([sys.stdin], [], [], 1)[0]
    if input:
        
        value = sys.stdin.readline().rstrip()
        
        length = len(value)
        if length > 3:
            cmd = value[0:3]
            data = value[3:length]
            
            if (cmd == "t1="):				# t1=nn.n 	PID 1 Target Deg
                target1 = data
                print ("PID 1 Target :", target1)
                PID_GainChangeFlag = True
                return (target1)
            
            elif (cmd == "p1="):			# p1=n.n 	PID 1 P value
                print ("PID 1 P Value")
                print (data)
                P1 = data
                PID_GainChangeFlag = True
                return (P1)
                
            elif (cmd == "i1="):			# i1=n.n 	PID 1 I value
                print ("PID 1 I Value")
                print (data)
                I1 = data
                PID_GainChangeFlag = True
                return (I1)
                
            elif (cmd == "d1="):			# d1=n.n 	PID 1 D value
                print ("PID 1 D Value")
                print (data)
                D1 = data
                PID_GainChangeFlag = True
                return (D1)
            
            if (cmd == "t2="):				# t1=nn.n 	PID 2 Target Deg
                print ("PID 2 Target")
                print (data)
                target2 = data
                PID_GainChangeFlag = True
                return (target2)
                
            elif (cmd == "p2="):			# p1=n.n 	PID 2 P value
                print ("PID 2 P Value")
                print (data)
                P2 = data
                PID_GainChangeFlag = True
                return (P2)
                
            elif (cmd == "i2="):			# i1=n.n 	PID 2 I value
                print ("PID 2 I Value")
                print (data)
                I2 = data
                PID_GainChangeFlag = True
                return (I2)
                
            elif (cmd == "d2="):			# d1=n.n 	PID 2 D value
                print ("PID 2 D Value")
                print (data)
                D2 = data
                PID_GainChangeFlag = True
                return (D2)
            
            if (cmd == "t3="):				# t1=nn.n 	PID 3 Target Deg
                print ("PID 3 Target")
                print (data)
                target3 = data
                PID_GainChangeFlag = True
                return (target3)
                
            elif (cmd == "p3="):			# p1=n.n 	PID 3 P value
                print ("PID 3 P Value")
                print (data)
                P3 = data
                PID_GainChangeFlag = True
                return (P3)
                
            elif (cmd == "i3="):			# i1=n.n 	PID 3 I value
                print ("PID 3 I Value")
                print (data)
                I3 = data
                PID_GainChangeFlag = True
                return (I3)
                
            elif (cmd == "d3="):			# d1=n.n 	PID 3 D value
                print ("PID 3 D Value")
                print (data)
                D3 = data
                PID_GainChangeFlag = True
                return (D3)
            
        elif (value == "r1"):
            PID1_run_state = not(PID1_run_state)
            print("PID 1 Run: ", PID1_run_state)
            heater1_state = False 
            return (PID1_run_state)
        
        elif (value == "r2"):
            PID2_run_state = not(PID2_run_state)
            print("PID 2 Run: ", PID2_run_state)
            heater2_state = False
            return (PID2_run_state)
        
        elif (value == "r3"):
            PID3_run_state = not(PID3_run_state)
            print("PID 3 Run: ", PID3_run_state)
            heater3_state = False
            return (PID3_run_state)
        
        elif (value == "h1"):
            heater1_state = not(heater1_state)
            Zoe_Outputs.heater1(heater1_state)
            print("Heater 1 On: ", heater1_state)
            return (heater1_state)
        
        elif (value == "h2"):
            heater2_state = not(heater2_state)
            Zoe_Outputs.heater2(heater2_state)
            print("Heater 2 on: ", heater2_state)        
            return (heater3_state)
        
        elif (value == "h3"):
            heater3_state = not(heater3_state)
            Zoe_Outputs.heater3(heater3_state)
            print("Heater 3 on: ", heater3_state)
            return (heater3_state)
        
        elif (value == "p"):
            pizo_state = not(pizo_state)
            Zoe_Outputs.alarm_pizo(pizo_state)
            print()
            print("pizo on: ", pizo_state)
            return(pizo_state)
        
        elif (value == "k"):
            print()
            print("Kill - Shutdown Pizo, PID & Heaters")
            PID1_run_state = False
            PID2_run_state = False
            PID3_run_state = False
            heater1_state = False
            Zoe_Outputs.heater1(heater1_state)
            heater2_state = False
            Zoe_Outputs.heater2(heater2_state)
            heater3_state = False
            Zoe_Outputs.heater2(heater2_state)
            pizo_state=False
            Zoe_Outputs.alarm_pizo(pizo_state)
            return()
            
        elif (value == "l"):
            print()
            print("Load config")
            #init()							#used during developmet
            Zoe_ConfigFile.openfile()
            return
            
        elif (value == "s"):
            print()
            print("Save Config")
            Zoe_ConfigFile.savefile()

        elif (value == "q"):
            print()
            print ("Exiting")
            sys.exit (0)
    
        elif (value == "?"):
            print("help.txt")
            print(Zoe_Help_text.helptxt)
            return ()
           
        else:
            print()
            print ("cmd unknown: %s" % value)
