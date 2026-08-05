#ZoE: help file txt
#================================================================
# 12-10-20  V17             		// This is the help display window text
helptxt = """
===============================================================================
24-9-25  Zoe V20 by Richard Nicholson, New Zealand

Raspbery Pi ver 3B+ over clocked
Uses 3 x  1 wire DS18B20 Temperature chips -55 to 125 deg
To feed 3 PID loops, to control 3 x Heat bands (PID output)
3 x GPIO pins connected to Solid State Relays (SSR-40 DA) to control Heat bands
1 x Pizo alarm via 3v gate Mosfet Module

Operation:
PID output zalue must get above the 'PID threshhold' for the heater to come on.
Load and Save configuration data to: /Defaults.txt

Each PID has a Target temperature value, PID Gain value,
Heater toggel flag, and Pizo toggel flag.

CLI COMMANDS
 ?		Help
 k		Kill - Shutdown Heaters, PIDs, Pizo
 l		Load config file
 s		Save config file
 p		Pizo On/Off Toggel		
 h1		Heater 1 On/Off Toggel
 h2		Heater 2 On/Off Toggel
 h3		Heater 3 On/Off Toggel
 r1		Run PID 1 Toggel On/Off
 r2		Run PID 2 Toggel On/Off
 r3		Run PID 3 Toggel On/Off
 q 		Quit
 t1=nn.n	Target Temp PID 1 Target Deg
 p1=n.n	P 	PID 1 P Gain 
 i1=n.n	I 	PID 1 I Gain
 d1=n.n	D 	PID 1 D Gain
 
===========================================================================
"""