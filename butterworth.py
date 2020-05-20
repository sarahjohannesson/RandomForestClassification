import sklearn
import csv
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#load dataset to a nympy-array
with open('acceleration_Person-O_OrderNumber-O-18(2).csv', 'r') as file:
 har = list(csv.reader(file))
 #first_row = np.array(har[0:1], dtype=np.string)
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'acc_x': har[ :,0],
    'acc_y': har[ :,1],
    'acc_z': har[ :,2],
    'time':har[ :,3]
})
data.head()

#Butterworth filter parameters
nmbr_samples = data['acc_x'].size
sec1 = har[ 0, 3 ]
sec2 = har [nmbr_samples-1,3]
print(sec2<sec1)
print(sec1)
print(sec2)
if(sec1>sec2):
    nmrsec = 60-sec1
    nmrsec = nmrsec + sec2
else:
    nmrsec = sec2 - sec1
print(nmrsec)
print(nmbr_samples)
fs = (nmbr_samples/nmrsec)
print(fs)
fc = 0.3


b, a = signal.butter(3, (fc/(fs/2)), 'low')     #FRÅGA Emma - vilken ordning??

filtx = signal.filtfilt(b,a, data['acc_x'])
filty = signal.filtfilt(b,a, data['acc_y'])
filtz = signal.filtfilt(b,a, data['acc_z'])

fgust = signal.filtfilt(b, a, data['acc_x'], method="gust")
fpad = signal.filtfilt(b, a, data['acc_x'], padlen=50)


#plt.plot(data['acc_x'],'g-', label='raw input')
#plt.plot(filtx, 'k-', label='filtered')
#plt.plot(fgust, 'b-', linewidth=4, label='gust')
#plt.plot(fpad, 'c-', linewidth=1.5, label='pad')
#plt.legend(loc='best')
#plt.title("Acc_x")
#plt.show()

#Sliding window - 128 bucket_size with 64 overlap count.
from window_slider import Slider
bucket_size = 1
overlap_count = 0
slider1 = Slider(bucket_size,overlap_count)
slider2 = Slider(bucket_size,overlap_count)
slider3 = Slider(bucket_size,overlap_count)
slider4 = Slider(bucket_size,overlap_count)
slider5 = Slider(bucket_size,overlap_count)
slider6 = Slider(bucket_size,overlap_count)
slider7 = Slider(bucket_size,overlap_count)

slider1.fit(filtx)
slider2.fit(filty)
slider3.fit(filtz)
slider4.fit(data['acc_x'].values)
slider5.fit(data['acc_y'].values)
slider6.fit(data['acc_z'].values)
slider7.fit(data['time'].values)

i = 1

while True:
    fx = slider1.slide()
    fy = slider2.slide()
    fz = slider3.slide()
    rx = slider4.slide()
    ry = slider5.slide()
    rz = slider6.slide()
    t = slider7.slide()

    bx = rx-fx
    by = ry -fy
    bz = rz -fz

    with open('Grav&Body_acceleration_Person-O_OrderNumber-O-18(2).csv', 'a', newline='' ) as f:
        writer = csv.writer(f)
        if (i == 1):
            writer.writerow([ "blank", "gravx", "gravy", "gravz", "bodyx", "bodyy", "bodyz", "time"] )
            i = 2
        writer.writerow( [ "%f\r\n" % (i), (fx), (fy), (fz), (bx), (by), (bz),t])
    if slider1.reached_end_of_list(): break




