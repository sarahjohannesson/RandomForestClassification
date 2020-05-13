import sklearn
import csv
import pandas as pd
import numpy as np
from scipy import signal
from  scipy.signal import medfilt
import matplotlib.pyplot as plt

#load dataset to a nympy-array
with open('acceleration_Person-C_OrderNumber-C-16.csv', 'r') as file:
 har = list(csv.reader(file))
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'acc_x': har[ :,0],
    'acc_y': har[ :,1],
    'acc_z': har[ :,2]
})
data.head()

#median filter
medfiltx = medfilt(data['acc_x'])
medfilty = medfilt(data['acc_y'])
medfiltz = medfilt(data['acc_z'])

plt.plot(data['acc_x'],'g-', label='raw input')
plt.plot(medfiltx, 'k-', label='median filtered')
plt.legend(loc='best')
plt.show()

#Butterworth filter parameters
fc = 20
fs = 50

b, a = signal.butter(3, (fc/(fs/2)), 'low')     #FRÅGA Emma - vilken ordning??

filtx = signal.filtfilt(b,a, medfiltx)
filty = signal.filtfilt(b,a, medfilty)
filtz = signal.filtfilt(b,a, medfiltz)

fgust = signal.filtfilt(b, a, data['acc_x'], method="gust")
fpad = signal.filtfilt(b, a, data['acc_x'], padlen=50)


plt.plot(data['acc_x'],'g-', label='raw input')
plt.plot(filtx, 'k-', label='filtered')
#plt.plot(fgust, 'b-', linewidth=4, label='gust')
#plt.plot(fpad, 'c-', linewidth=1.5, label='pad')
plt.legend(loc='best')
plt.show()

#Sliding window - 128 bucket_size with 64 overlap count.
from window_slider import Slider
bucket_size = 1
overlap_count = 0
slider1 = Slider(bucket_size,overlap_count)
slider2 = Slider(bucket_size,overlap_count)
slider3 = Slider(bucket_size,overlap_count)


slider1.fit(filtx)
slider2.fit(filty)
slider3.fit(filtz)
i = 1

while True:
    fx = slider1.slide()
    fy = slider2.slide()
    fz = slider3.slide()


    with open('AccFiltered20Hz.csv', 'a', newline='' ) as f:
        writer = csv.writer(f)
        if (i == 1):
            writer.writerow([ "blank", "filtx", "filty", "filtz"] )
            i = 2
        writer.writerow( [ "%f\r\n" % (i), (fx), (fy), (fz)])
    if slider1.reached_end_of_list(): break




