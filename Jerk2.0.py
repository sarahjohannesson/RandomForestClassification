import sklearn
import csv
import numpy as np
import pandas as pd

sample_freq = 51.14
#nbrOfSample = 1500
#recordingTime = 30
#timediff = recordingTime/nbrOfSample
timediff = 1/sample_freq

#load dataset a1 to a nympy-array
with open('Tot_Gyro_Freq_51.14.csv', 'r') as file:
 a1 = list(csv.reader(file))
 a1 = np.array(a1[1:], dtype=np.float)

# load dataset a2 to a nympy-array
with open( 'Tot_Gyro_Freq_51.14.csv', 'r' ) as file:
  a2 = list( csv.reader( file ) )
  a2 = np.array( a2[ 1: ], dtype=np.float )
  a2 = np.delete(a2, 0,0)

# seperate data
data = pd.DataFrame( {
 'a1x': a1[ :, 0 ],
 'a1y': a1[ :, 1 ],
 'a1z': a1[ :, 2 ]

} )
data.head()

#seperate data
data2 = pd.DataFrame( {
 'a2x': a2[ :, 0 ],
 'a2y': a2[ :, 1 ],
 'a2z': a2[ :, 2 ]
} )
data.head()

#sliding window - bucket_size 1 and overlap 0.
from window_slider import Slider
bucket_size = 1
overlap_count = 0
slider1 = Slider(bucket_size, overlap_count)
slider2 = Slider(bucket_size, overlap_count)
slider3 = Slider(bucket_size, overlap_count)
slider4 = Slider(bucket_size, overlap_count)
slider5 = Slider(bucket_size, overlap_count)
slider6 = Slider(bucket_size, overlap_count)
slider1.fit(data['a1x'].values)
slider2.fit(data2['a2x'].values)
slider3.fit(data['a1y'].values)
slider4.fit(data2['a2y'].values)
slider5.fit(data['a1z'].values)
slider6.fit(data2['a2z'].values)
i = 1

while True:
  a1x = slider1.slide()
  a2x = slider2.slide()
  subx = np.subtract(a2x,a1x)
  jerkx = ((subx)/timediff )

  a1y = slider3.slide()
  a2y = slider4.slide()
  suby = np.subtract(a2y,a1y)
  jerky = ((suby)/timediff )

  a1z = slider5.slide()
  a2z = slider6.slide()
  subz = np.subtract(a2z,a1z)
  jerkz = ((subz)/timediff )

  # swrite to csv-file.
  with open('Tot_GyroJerk_Freq_51.14.csv', 'a', newline='' ) as f:
     writer = csv.writer( f )
     if (i==1):
        writer.writerow(["blank","Jerk-X", "Jerk-Y" ,"Jerk-Z"])
        i = 2
     writer.writerow(["%f\r\n" % i,(jerkx), (jerky),(jerkz)])
  if slider2.reached_end_of_list(): break
