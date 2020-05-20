import csv
import pandas as pd
import numpy as np


#load dataset to a nympy-array
with open('Grav_acceleration_OrderNumber-P-37.csv', 'r') as file:
 har = list(csv.reader(file))
 #first_row = np.array(har[0:1], dtype=np.string)
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'acc_x': har[ :,0],
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