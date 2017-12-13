import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r--', animated=True)

def init():
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 120)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(frame)
    ln.set_data(xdata, ydata)
    return ln,


anim = FuncAnimation(fig, update, frames=100, interval=20,
                        init_func=init, blit=True, repeat=False)

plt.show()