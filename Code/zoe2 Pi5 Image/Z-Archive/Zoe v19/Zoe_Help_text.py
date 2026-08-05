#ZoE: help file txt
#================================================================
# 12-10-20  V17             		// This is the help display window text
helptxt = """
24-9-25  V19  ZoE, Richard Nicholson, New Zealand

Uses 3 x PID loops to control 3 heater bands via 3 x temperature sensors

Uses 3 thermocouples, to measure temperature, via 3 x DS18B20 chips (Adreno accesory kitset).
Three GPIO pins connected to Solid State Relays (SSR-40 DA) to control Heat bands (PID output).
An alarm buzzer will sound if the PID power output gets to high, ie heater not working.

Operation:
Program starts in full screen mode, (<F11> toggels full screen), its written to work on 7" touch screen
It will imediately start graphing temperatures and PID output = zero on startup.
Use Preheat/manual button to start a PID. Once temperature is at 'n' deg C, below the target temperature
the preheat stage will finish and the PID run LED will com on, and PID calcultaion will start.
PID output value must get above the 'PID output threshhold' before the heater will come back on.


Each PID has a Run button, Target temperature, PID variables, Output on/off indicator, and Alarm output buzzer.

It then turns associated PID off. 
It can be put into Manual control, allowing the Heater outputs to be turned on/off individualy.


Sofware
    <ESC>   End GUI
    <F11>   Toggel full screen
    <ENTER>  To load values in entry fields

Configuration file allowing different profile settings for defferent plastics, to be saved for later use.
Reads and Writes configuration data to disk file.
Hard coded startup file is: /Defaults.txt
    

HARDWARE:
Raspbery Pi ver 3B
3 x DS18B20 -55 to 125 Deg probe. Adreno accesory kitset.
3 x GPIO pins (heater output). These are connected directly to SSR-40 DA solid state relays. 3 volt input.
1 x Pizo Buzzer
1 x 7" touch screen (optional but recomended)

If using a 7" touch screen it is recommend to install a vertual keyboard
https://pimylifeup.com/raspberry-pi-on-screen-keyboard/

Original code Source - this is a very helpfull link.
https://www.digikey.co.uk/en/maker/projects/python-gui-guide-introduction-to-tkinter/d04a764c78114682aac9255056026338

"""