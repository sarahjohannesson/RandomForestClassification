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

nbrOfSample = 1500      #Kolla vad sample från backend
recordingTime = 30
timediff = recordingTime/nbrOfSample
sample_rate = nbrOfSample / recordingTime
sum_freq =  0
index_freq = 0

#load dataset to a nympy-array
with open('Rörelse - 6 - BodyAccJerk-XYZ.csv', 'r') as file:        #Test_Y&E data-cvs
 har = list(csv.reader(file))
 #first_row = np.array(har[0:1], dtype=np.string)
 har = np.array(har[1:], dtype=np.float)

#seperate data
data=pd.DataFrame({
    'x': har[ :,0],
    'y': har[ :,1],
    'z': har[ :,2]
})
data.head()

#Sliding window - 128 bucket_size with 64 overlap count.
from window_slider import Slider
bucket_size = 128
overlap_count = 64
slider1 = Slider(bucket_size,overlap_count)
slider2 = Slider(bucket_size,overlap_count)
slider3 = Slider(bucket_size,overlap_count)
slider1.fit(data['x'])
slider2.fit(data['y'])
slider3.fit(data['z'])
i = 1
while True:
    x = slider1.slide()
    y = slider2.slide()
    z = slider3.slide()
                                #byt till rfft. OBS! Kolla om jag vekrligen behöver abs. Sen använd fft.fft.freq för att dubblkolla att frekvenserna stämme.r
    #FFT - transform görs på vekorn, eller ska det göras separat på varje värde? Får väldigt olika värden.
    fft_x = abs(np.fft.rfft(x))  #ta absolut värdet eller bara real-delen.
    fft_y = abs(np.fft.rfft(y))
    fft_z = abs(np.fft.rfft(z))

    fft_x_freq = np.fft.rfftfreq( x.size, d=1./sample_rate )   #ger freq-vektorn.
    fft_y_freq = np.fft.rfftfreq( y.size, d=1./sample_rate )
    fft_z_freq = np.fft.rfftfreq( z.size, d=1./sample_rate )

    #size på fre och på fft
    n = fft_x.size     #65
    n_freq = fft_z_freq.size  #65 för Y&E         OBS! Kolla vad ärdena

    #Calculate values to cvs-file

    meanx = st.mean(fft_x)
    meany = st.mean(fft_y)
    meanz = st.mean(fft_z)

    mad1x = pd.Series(fft_x)
    madx = mad1x.mad()
    mad1y = pd.Series(fft_y)
    mady = mad1y.mad()
    mad1z = pd.Series(fft_z)
    madz = mad1z.mad()

    maxx = max(fft_x)
    maxy = max(fft_y)
    maxz = max(fft_z)

    minx = min(fft_x)
    miny = min(fft_y)
    minz = min(fft_z)

    stdx = st.stdev(fft_x)
    stdy = st.stdev(fft_y)
    stdz = st.stdev(fft_z)

    iqx = iqr(fft_x)
    iqy = iqr(fft_y)
    iqz = iqr(fft_z)

    #Calculate signal entropy
    sx = pd.Series(fft_x)
    vectorx = (sx.groupby( sx ).transform('count') / len( sx )).values
    entrox = entropy(vectorx)
    sy = pd.Series(fft_y)
    vectory = (sy.groupby( sy ).transform('count') / len( sy )).values
    entroy = entropy( vectory )
    sz = pd.Series(fft_z)
    vectorz = (sz.groupby( sz ).transform('count') / len( sz )).values
    entroz = entropy( vectorz )

    #Calculate signal energy
    resx = sum(map(lambda i: i * i, fft_x))
    energyx = resx/(fft_x.size)
    resy = sum( map( lambda i: i * i,fft_y) )
    energyy = resy / (fft_y.size)
    resz = sum( map( lambda i: i * i,fft_z ) )
    energyz = resz / (fft_z.size)

    #Calculate SMA
    integralx = np.trapz(fft_x, dx=timediff)
    integraly = np.trapz(fft_y, dx=timediff)
    integralz = np.trapz(fft_z, dx=timediff)
    t = timediff*(x.size)
    SMA = (1/t)*(integralx+integraly+integralz)

    skx = skew(fft_x)
    skz = skew(fft_y)
    sky = skew(fft_z)

    kx = kurtosis(fft_x)
    ky = kurtosis(fft_y)
    kz = kurtosis(fft_z)

    # maxInds -- Largest frequency component.
    resultx = np.where(fft_x == maxx)
    indexx = resultx[0][0]  # väljer platsen första gången max (=magnitude pga abs) förekommer
    max_Inds_x = fft_x_freq.item(indexx)
    resulty = np.where(fft_y == maxy)
    indexy = resulty[0][0]
    max_Inds_y = fft_y_freq.item(indexy)
    resultz = np.where(fft_z == maxz)
    indexz = resultz[0][0]
    max_Inds_z = fft_z_freq.item( indexz )

    #meanFreq
    for x in np.nditer(fft_x) :
        freq = fft_x_freq.item(index_freq)
        sum_freq = sum_freq + (x * freq)
        index_freq = index_freq + 1
    meanfreq_x = sum_freq/(sum(fft_x))
    sum_freq = 0
    index_freq = 0

    for y in np.nditer(fft_y) :
        freq = fft_y_freq.item(index_freq)
        sum_freq = sum_freq + (y * freq)
        index_freq = index_freq + 1
    meanfreq_y = sum_freq/(sum(fft_y))
    sum_freq = 0
    index_freq = 0

    for z in np.nditer(fft_z) :
        freq = fft_z_freq.item(index_freq)
        sum_freq = sum_freq + (z * freq)
        index_freq = index_freq + 1
    meanfreq_z = sum_freq/(sum(fft_z))
    sum_freq = 0
    index_freq = 0

    # skriv in i csv-file.
    with open('Rörelse - 6 - fBodyAccJerk-XYZ.csv', 'a', newline='' ) as f:
        writer = csv.writer( f )
        if (i==1):
            writer.writerow(["blank", "mean-x", "mean-y", "mean-z", "std-x", "std-y", "std-z", "mad-x", "mad-y", "mad-z","max-x","max-y", "max-z", "min-x", "min-y", "min-z", "sma", "energy-x", "energy-y", "energy-z", "iqr-x", "iqr-y", "iqr-z", "entropy-x", "entropy-y", "entropy-z", "maxInds-x", "maxInds-y", "maxInds-z", "meanFreq-x", "meanFreq-y", "meanFreq-z", "skewness-x", "kurtisos-x", "skewness-y", "kurtisos-y", "skewness-z", "kurtisos-z"])
            i = 2
        writer.writerow(["%f\r\n" % (i), (meanx), (meany), (meanz), (stdx), (stdy), (stdz), (madx), (mady), (madz), (maxx), (maxy), (maxz), (minx), (miny), (minz), (SMA), (energyx), (energyy), (energyz), (iqx), (iqy), (iqz), (entrox), (entroy), (entroz), (max_Inds_x), (max_Inds_y), (max_Inds_z), (meanfreq_x), (meanfreq_y), (meanfreq_z), (skx), (kx), (sky), (ky), (skz), (kz)])
    if slider1.reached_end_of_list(): break


