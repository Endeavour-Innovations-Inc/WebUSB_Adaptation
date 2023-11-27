import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import numpy as np
import csv
import usb.core

#from scipy import signal

import scope_interface

scope_interface.connect_to_scope()

t_data = []
v_data = []

data_ready = None
while(data_ready == None):
    try:
        data_ready = scope_interface.check_for_data()
    except usb.core.USBError:
        print('Error Encountered - Retrying')
        pass

print('Interrupt Received From Device - Requesting Data...')

v_data = scope_interface.get_samples()
print(len(v_data))

t_data = np.arange(0, len(v_data), 1)
#print(t_data)

#signal filtering
#b, a = signal.butter(3, 0.025)
#zi = signal.lfilter_zi(b, a)
#y_filt = signal.filtfilt(b, a, v_data)


class SnappingCursor:
    
    #A cross-hair cursor that snaps to the data point of a line, which is
    #closest to the *x* position of the cursor.

    #For simplicity, this assumes that *x* values of the data are sorted.
    
    def __init__(self, ax, line):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.x, self.y = line.get_data()
        self._last_index = None
        # text location in axes coords
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.x, x), len(self.x) - 1)
            if index == self._last_index:
                return  # still on the same data point. Nothing to do.
            self._last_index = index
            x = self.x[index]
            y = self.y[index]
            # update the line positions
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.text.set_text(f'x={x:1.2f}, y={y:1.2f}')
            self.ax.figure.canvas.draw()

fig, ax = plt.subplots()
ax.set_title('Sampled Data (' + str(int(len(v_data)/1000)) + 'K Samples)')
line, = ax.plot(t_data, v_data)
#line, = ax.plot(t_data, y_filt)
snap_cursor = SnappingCursor(ax, line)
fig.canvas.mpl_connect('motion_notify_event', snap_cursor.on_mouse_move)

# Simulate a mouse move to (0.5, 0.5), needed for online docs
t = ax.transData
MouseEvent(
    "motion_notify_event", ax.figure.canvas, *t.transform((0.5, 0.5))
)._process()

plt.show()






