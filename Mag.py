import sklearn
import csv
import numpy as np
import pandas as pd
from numpy.linalg import norm

#load dataset a1 to a nympy-array
with open('Tot_Body_Freq_51.14.csv', 'r') as file:
 har = list(csv.reader(file))
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'x': har[ :,0],
    'y': har[ :,1],
    'z': har[ :,2]
})
data.head()

#sliding window - 1 bucket_size with 0 overlap count.
from window_slider import Slider
bucket_size = 1
overlap_count = 0
slider1 = Slider(bucket_size, overlap_count)
slider2 = Slider(bucket_size, overlap_count)
slider3 = Slider(bucket_size, overlap_count)
slider1.fit(data['x'].values)
slider2.fit(data['y'].values)
slider3.fit(data['z'].values)
i = 1
while True:
  acc1 = slider1.slide()
  acc2 = slider2.slide()
  acc3 = slider3.slide()
  arr = np.array([acc1, acc2, acc3])
  mag = norm(arr)

  # write to csv-file.
  with open('Tot_BodyMag_Freq_51.14.csv', 'a', newline='' ) as f:
     writer = csv.writer( f )
     if (i==1):
        writer.writerow(["blank","AccMag"])
        i = 2
     writer.writerow(["%f\r\n" % (i),(mag)])
  if slider2.reached_end_of_list(): break

