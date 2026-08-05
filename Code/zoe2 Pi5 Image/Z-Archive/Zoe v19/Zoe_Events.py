#ZoE: GUI Events
#---------------------------------------------------------------------------------------
# Entry: filename value changed in GUI, Entry changed call back
def on_filename_changed(event):
    
    print ('at on_filename_changed')
    
    global filename                                          #filename
    
    # get target value and error chk
    try:
        value = int(entry_filename.get())
        print(value)
        filename = value
    except ValueError:
        print("Invalid Value in filename entry box")
    entry_filename.delete(0, 50)
    entry_filename.insert(0, filename)

    canvas.draw()

#---------------------------------------------------------------------------------------
# Entry: target1 value changed in GUI, Entry changed call back
def on_target1_changed(event):
    
    print ('at target1_changed')
    
    global target1                                          #target1 =
    global matchbox
    
    # get target value and error chk
    try:
        value = int(entry_target1.get())
        print(value)
        target1 = value
    except ValueError:
        print("Invalid Value in Target 1 entry box")
    entry_target1.delete(0, 5)
    entry_target1.insert(0, target1)

    os.close(matchbox)
    
    canvas.draw()

#------------------------------------------------------------------------------------
# Entry: P1 value changed in GUI, Entry changed call back
def on_P1_changed(event):
    
    print ('at on_P1_changed')
    
    global P1
    
    # get P1 value and error chk
    try:
        value = float(entry_P1.get())
        print(value)
        P1 = value
    except ValueError:
        print("Invalid Value in P1 entry box")
    entry_P1.delete(0, 5)
    entry_P1.insert(0, P1)

    canvas.draw()

#-----------------------------------------------------------------------------------
# Entry: I1 value changed in GUI, Entry changed call back
def on_I1_changed(event):
    
    print ('at on_I1_changed')
    
    global I1
    
    # get I1 value and error chk
    try:
        value = float(entry_I1.get())
        print(value)
        I1 = value
    except ValueError:
        print("Invalid Value in I1 entry box")
    entry_I1.delete(0, 5)
    entry_I1.insert(0, I1)

    canvas.draw()

#-----------------------------------------------------------------------------------
# Entry: D1 value changed in GUI, Entry changed call back
def on_D1_changed(event):
    
    print ('at on_D1_changed')
    
    global D1
    
    # get D1 value and error chk
    try:
        value = float(entry_D1.get())
        print(value)
        D1 = value
    except ValueError:
        print("Invalid Value in D1 entry box")
    entry_D1.delete(0, 5)
    entry_D1.insert(0, D1)

    canvas.draw()

#----------------------------------------------------------------------------------------
# Entry: target2 value changed in GUI, Entry changed call back
def on_target2_changed(event):

    print ('at on_target2_changed')
    
    global target2                                  #target2
    
    # get target value and error chk
    try:
        value = int(entry_target2.get())
        print(value)
        target2 = value
    except ValueError:
        print("Invalid Value in Target 2 entry box")
    entry_target2.delete(0, 5)
    entry_target2.insert(0, target2)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: P2 value changed in GUI, Entry changed call back
def on_P2_changed(event):
    
    print ('at on_P2_changed')
    
    global P2
    
    # get P2 value and error chk
    try:
        value = float(entry_P2.get())
        print(value)
        P2 = value
    except ValueError:
        print("Invalid Value in P2 entry box")
    entry_P2.delete(0, 5)
    entry_P2.insert(0, P2)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: I2 value changed in GUI, Entry changed call back
def on_I2_changed(event):

    print ('at on_I2_changed')
    
    global I2
    
    # get I2 value and error chk
    try:
        value = float(entry_I2.get())
        print(value)
        I2 = value
    except ValueError:
        print("Invalid Value in I2 entry box")
    entry_I2.delete(0, 5)
    entry_I2.insert(0, I2)

    canvas.draw()

#---------------------------------------------------------------------------------
# Entry: D2 value changed in GUI, Entry changed call back
def on_D2_changed(event):

    print ('at on_D2_changed')
    
    global D2
    
    # get D2 value and error chk
    try:
        value = float(entry_D2.get())
        print(value)
        D2 = value
    except ValueError:
        print("Invalid Value in D2 entry box")
    entry_D2.delete(0, 5)
    entry_D2.insert(0, D2)

    canvas.draw()

#-------------------------------------------------------------------------------------
# Entry: target3 value changed in GUI, Entry changed call back
def on_target3_changed(event):

    print ('at on_target3_changed')
    
    global target3                              #target3 = 
    
    # get target value and error chk
    try:
        value = int(entry_target3.get())
        print(value)
        target3 = value
    except ValueError:
        print("Invalid Value in Target 3 entry box")
    entry_target3.delete(0, 5)
    entry_target3.insert(0, target3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: P3 value changed in GUI, Entry changed call back
def on_P3_changed(event):

    print ('at on_P3_changed')
    
    global P3
    
    # get P3 value and error chk
    try:
        value = float(entry_P3.get())
        print(value)
        P3 = value
    except ValueError:
        print("Invalid Value in P3 entry box")
    entry_P3.delete(0, 5)
    entry_P3.insert(0, P3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: I3 value changed in GUI, Entry changed call back
def on_I3_changed(event):

    print ('at on_I3_changed')
    
    global I3
    
    # get I3 value and error chk
    try:
        value = float(entry_I3.get())
        print(value)
        I3 = value
    except ValueError:
        print("Invalid Value in I3 entry box")
    entry_I3.delete(0, 5)
    entry_I3.insert(0, I3)

    canvas.draw()

#------------------------------------------------------------------------------
# Entry: D3 value changed in GUI, Entry changed call back
def on_D3_changed(event):

    print ('at on_D3_changed')
    
    global D3
    
    # get D3 value and error chk
    try:
        value = float(entry_D3.get())
        print(value)
        D3 = value
    except ValueError:
        print("Invalid Value in D3 entry box")
    entry_D3.delete(0, 5)
    entry_D3.insert(0, D3)

    canvas.draw()
