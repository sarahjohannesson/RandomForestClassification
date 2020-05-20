import csv
import pandas as pd
import numpy as np


#load dataset to a nympy-array
with open('Grav&Body_acceleration_Person-G_OrderNumber-G-27(2).csv', 'r') as file:
 har = list(csv.reader(file))
 #first_row = np.array(har[0:1], dtype=np.string)
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'acc_x': har[ :,0],
    'acc_y': har[ :,1],
    'acc_z': har[ :, 2 ],
    'grav_x': har[ :, 3 ],
    'grav_y': har[ :,4],
    'grav_z': har[ :, 5 ],
    'time':har[ :,6]
})
data.head()

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


slider1.fit(data['acc_x'].values)
slider2.fit(data['acc_y'].values)
slider3.fit(data['acc_z'].values)
slider4.fit(data['grav_x'].values)
slider5.fit(data['grav_y'].values)
slider6.fit(data['grav_z'].values)
slider7.fit(data['time'].values)
i = 1

while True:
    gx = slider1.slide()
    gy = slider2.slide()
    gz = slider3.slide()
    ax = slider4.slide()
    ay = slider5.slide()
    az = slider6.slide()
    t = slider7.slide()


    with open('Body_acceleration_OrderNumber-G-27(2).csv', 'a', newline='' ) as f1:
        writer1 = csv.writer(f1)
        if (i == 1):
            writer1.writerow([ "blank", "bodyx", "bodyy", "bodyz", "timestamp"] )
            i = 2
        writer1.writerow( [ "%f\r\n" % (i), (ax), (ay), (az), t])
    #if slider1.reached_end_of_list(): break

    with open('Grav_acceleration_OrderNumber-G-27(2).csv', 'a', newline='' ) as f2:
        writer2 = csv.writer(f2)
        if (i == 1):
            writer2.writerow([ "blank", "gravx", "gravy", "gravz", "timestamp"] )
            i = 2
        writer2.writerow( [ "%f\r\n" % (i), (gx), (gy), (gz), t])
    if slider1.reached_end_of_list(): break
