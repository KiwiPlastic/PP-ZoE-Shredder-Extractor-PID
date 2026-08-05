# Change default figure size. 
# Adsolute positioning has something to do with the back end
# set x and y to set position
import matplotlib
import matplotlib.pyplot as plt

print (plt.rcParams.get('figure.figsize'))

fig_size = plt.rcParams["figure.figsize"]
# default size is 6.4 x 4.8
fig_size[0] = 6
fig_size[1] = 4.8
plt.rcParams["figure.figsize"] = fig_size

backend = matplotlib.get_backend()

print (backend)
print ()
print(plt.rcParams.get("figure.figsize" ))

#fig = plt.figure(figsize=(6,8))

f1 = plt.figure(1)                                  # this line sets the focus to fig 1, then build the graph frame work
#f1 = plt.figure(1, figsize = (100,110))        #this does not error, but also does not work

# set Absolute figure position, this cas etop left corner
#x = 500
#y = 500
x = 10
y = 35
ax1 = f1.add_subplot(1, 1, 1)
#f1.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))

plt.show()
