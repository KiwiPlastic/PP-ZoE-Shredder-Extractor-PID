import matplotlib
import matplotlib.pyplot as plt

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

f, ax = plt.subplots()
move_figure(f, 500, 500)
plt.show()

# another example
fig = figure()
fig.canvas.manager.window.Move(100,400)


#another example, using images with plot
fig.savefig('abc.png')
from PIL import Image
im = Image.open("abc.jpg")
im.rotate(0).show()

# and anouther

import matplotlib  
matplotlib.use("TkAgg") # set the backend  

if backend == 'TkAgg':  
    f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))


