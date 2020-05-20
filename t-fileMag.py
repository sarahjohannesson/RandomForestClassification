import sklearn
import csv
import pandas as pd
import numpy as np
import statistics as st
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import entropy
from scipy.stats import iqr
from numpy import corrcoef

#nbrOfSample = 1500
#recordingTime = 30
#timediff = recordingTime/nbrOfSample
sample_rate = 51.14
timediff = 1/sample_rate

#load dataset to a nympy-array
with open('Tot_GravMag_Freq_51.14.csv', 'r') as file:
 har = list(csv.reader(file))
 #first_row = np.array(har[0:1], dtype=np.string)
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'mag': har[ :,0]
})
data.head()

#Sliding window - 128 bucket_size with 64 overlap count.
from window_slider import Slider
bucket_size = 128
overlap_count = 64
slider1 = Slider(bucket_size,overlap_count)
slider1.fit(data['mag'])
i = 1
while True:
    x = slider1.slide()

    #Calculate values to cvs-file
    meanx = st.mean(x)
    mad1x = pd.Series(x)
    madx = mad1x.mad()
    maxx = max(x)
    minx = min(x)
    stdx = st.stdev(x)
    iqx = iqr(x)

    #Calculate signal entropy
    sx = pd.Series(x)
    vectorx = (sx.groupby( sx ).transform( 'count' ) / len( sx )).values
    entrox = entropy(vectorx)

    #Calculate signal energy
    resx = sum(map(lambda i: i * i, x))
    energyx = resx/(x.size)

    #Calculate SMA
    integralx = np.trapz(x, dx=timediff)
    t = timediff*(x.size)
    SMA = (1/t)*(integralx)

    # write to csv-file
    with open('Tot_tGravMag_Freq_51.14.csv', 'a', newline='' ) as f:
        writer = csv.writer( f )
        if (i==1):
            writer.writerow(["blank", "mean", "std", "mad", "max", "min", "sma", "energy","iqr","entropy"])
            i = 2
        writer.writerow(["%f\r\n" % (i), (meanx), (stdx), (madx), (maxx), (minx),(SMA), (energyx), (iqx),(entrox)])
    if slider1.reached_end_of_list(): break


