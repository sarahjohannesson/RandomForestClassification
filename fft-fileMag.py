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
sum_freq =  0
index_freq = 0

#load dataset to a nympy-array
with open('Tot_GyroJerkMag_Freq_51.14.csv', 'r') as file:
 har = list(csv.reader(file))
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
    fft_x = abs(np.fft.rfft(x))
    n = fft_x.size

    #sample_rate = nbrOfSample/recordingTime
    fft_x_freq = np.fft.rfftfreq(x.size, d=1./sample_rate)    

    #Calculate values to cvs-file
    meanx = st.mean(fft_x)
    mad1x = pd.Series(fft_x)
    madx = mad1x.mad()
    maxx = max(fft_x)
    #print("max", maxx)
    minx = min(fft_x)
    stdx = st.stdev(fft_x)
    iqx = iqr(fft_x)
    #Calculate signal entropy
    sx = pd.Series(fft_x)
    vectorx = (sx.groupby( sx ).transform( 'count' ) / len( sx )).values
    entrox = entropy(vectorx)
    #Calculate signal energy
    resx = sum(map(lambda i: i * i, fft_x))
    energyx = resx/(fft_x.size)

    #Calculate SMA
    integralx = np.trapz(fft_x, dx=timediff)
    t = timediff*(fft_x.size)
    SMA = (1/t)*(integralx)

    #skewness & kurtosis
    sk = skew(fft_x )
    k = kurtosis(fft_x)

    #maxInds
    resultx = np.where( fft_x == maxx )
    indexx = resultx[ 0 ][ 0 ] 
    max_Inds = fft_x_freq.item( indexx )

    #meanFreq
    for x in np.nditer(fft_x) :
        freq = fft_x_freq.item(index_freq)
        sum_freq = sum_freq + (x * freq)
        index_freq = index_freq + 1
    meanfreq_x = sum_freq/(sum(fft_x))
    sum_freq = 0
    index_freq = 0


    # skriv in i csv-file.
    with open('Tot_fGyroJerkMag_Freq_51.14.csv', 'a', newline='' ) as f:
        writer = csv.writer( f )
        if (i==1):
            writer.writerow(["blank", "mean", "std", "mad", "max", "min", "sma", "energy","iqr","entropy", "maxInds", "meanFreq", "skewness", "kurtosis"])
            i = 2
        writer.writerow(["%f\r\n" % (i), (meanx), (stdx), (madx), (maxx), (minx),(SMA), (energyx), (iqx),(entrox), (max_Inds), (meanfreq_x),(sk), (k)])
    if slider1.reached_end_of_list(): break


