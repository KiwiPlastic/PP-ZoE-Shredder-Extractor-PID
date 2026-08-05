#ZoE: GUI Bindings, this is used by tk (GUI)
#---------------------------------------------------------------------------------------
# Binding: Toggle fullscreen, triggered by pressing <F11>
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)

#---------------------------------------------------------------------------------------
# Binding: 
def on_target1_focus(event):

    print(" at on_target1_focus")
    
    global os
    global matchbox
    
    matchboxstr = 'matchbox-keyboard'
    matchbox = os.popen(matchboxstr, 'w')
    print ('matchbox ', (matchbox))
    #matchbox = os.popen('toggle-keyboard')
    
#-------------------------------------------------------------------------------------
# Binding: Return to windowed mode, not used
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

#--------------------------------------------------------------------------------------
# Binding: Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 35)))
    dfont.configure(size=new_size)
    
#------------------------------------------------------------------------------------------------------    
# Binding: comes here to terminate GUI if <ESC> key pressed
def end(event):
    
    HEATER1.off()
    HEATER2.off()
    HEATER3.off()
    ALMBUZZER.off()
    pass
    root.destroy()

#-------------------------------------------------------------------------------------------------------
# Binding: Dummy function prevents segfault, clicking 'quit' comes here
def _destroy(event):
    
    HEATER1.off()
    HEATER2.off()
    HEATER3.off()
    ALMBUZZER.off()
    pass
