import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import numpy as np
import csv

from scipy import signal

#pyusb setup
import usb.core
import usb.util
import usb.backend.libusb1
import sys

backend = usb.backend.libusb1.get_backend(find_library=lambda x: "./libusb-1.0.dll")
dev = usb.core.find(backend=backend)

dev = usb.core.find(idVendor=0x1fc9, idProduct=0x000C)
if dev is None:
    raise ValueError('Our device is not connected')

print(dev)

cfg = usb.util.find_descriptor(dev, bConfigurationValue=1)
cfg.set()

#print(cfg)

try:
    dev.set_interface_altsetting(interface = 0, alternate_setting = 0x0)
except USBError:
    pass

for bRequest in range(255):
    try:
        read = dev.ctrl_transfer(0x80, bRequest, 0, 0, 16) #read 8 bytes
        print ("bRequest ", bRequest)
        print (read)
    except:
        # failed to get data for this request
        pass

"""

t_data = []
v_data = []

with open('noisy_sin_gen.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
    header = next(reader, None)  # skip the headers, save to 'header'
    for row in reader:
        t_data.append(float(row[0]))
        v_data.append(float(row[1]))

#print(header)
print(t_data)
print(v_data)


b, a = signal.butter(3, 0.025)
zi = signal.lfilter_zi(b, a)
y_filt = signal.filtfilt(b, a, v_data)

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
ax.set_title('Snapping cursor')
#line, = ax.plot(t_data, v_data)
line, = ax.plot(t_data, y_filt)
snap_cursor = SnappingCursor(ax, line)
fig.canvas.mpl_connect('motion_notify_event', snap_cursor.on_mouse_move)

# Simulate a mouse move to (0.5, 0.5), needed for online docs
t = ax.transData
MouseEvent(
    "motion_notify_event", ax.figure.canvas, *t.transform((0.5, 0.5))
)._process()

plt.show()

"""



