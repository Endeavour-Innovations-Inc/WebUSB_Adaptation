import matplotlib.pyplot as plt
import scipy.signal
import plotly.express as px
import plotly.subplots
import plotly.graph_objects as go
import csv

from scipy import signal
from plotly.subplots import make_subplots

t_data = []
v_data = []

with open('noisy_sin_gen.csv', newline='') as csvfile:
#with open('tri_gen.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
    next(reader, None)  # skip the headers
    for row in reader:
        t_data.append(float(row[0]))
        v_data.append(float(row[1]))
print(t_data)
print(v_data)


b, a = signal.butter(3, 0.05)
zi = signal.lfilter_zi(b, a)
y_filt = signal.filtfilt(b, a, v_data)


plt.plot(t_data, v_data)
plt.plot(t_data, y_filt)
plt.show()


"""
fig = px.line(x=t_data, y=v_data)
fig.add_scatter(x=t_data, y=y_filt)
fig.show()
"""
