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
with open('Tot_Grav_Freq_51.14.csv', 'r') as file:        
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

    #Calculate values to cvs-file
    meanx = st.mean(x)
    meany = st.mean(y)
    meanz = st.mean(z)

    mad1x = pd.Series(x)
    madx = mad1x.mad()
    mad1y = pd.Series(y)
    mady = mad1y.mad()
    mad1z = pd.Series(z)
    madz = mad1z.mad()

    maxx = max(x)
    maxy = max(y)
    maxz = max(z)

    minx = min(x)
    miny = min(y)
    minz = min(z)

    stdx = st.stdev(x)
    stdy = st.stdev(y)
    stdz = st.stdev(z)

    iqx = iqr(x)
    iqy = iqr(y)
    iqz = iqr(z)

    #Calculate signal entropy
    sx = pd.Series(x)
    vectorx = (sx.groupby( sx ).transform( 'count' ) / len( sx )).values
    entrox = entropy(vectorx)
    sy = pd.Series(y)
    vectory = (sy.groupby( sy ).transform( 'count' ) / len( sy )).values
    entroy = entropy( vectory )
    sz = pd.Series( z )
    vectorz = (sz.groupby( sz ).transform( 'count' ) / len( sz )).values
    entroz = entropy( vectorz )

    #Calculate signal energy
    resx = sum(map(lambda i: i * i, x))
    energyx = resx/(x.size)
    resy = sum( map( lambda i: i * i, y ) )
    energyy = resy / (y.size)
    resz = sum( map( lambda i: i * i, z ) )
    energyz = resz / (z.size)


    #Calculate SMA
    integralx = np.trapz(x, dx=timediff)
    integraly = np.trapz(y, dx=timediff)
    integralz = np.trapz(z, dx=timediff)
    t = timediff*(x.size)
    SMA = (1/t)*(integralx+integraly+integralz)

    #correlation x-y,x-z
    corr_x_y = corrcoef(x,y)
    corr_x_z = corrcoef(x,z)
    corr_y_z = corrcoef(y,z)
    corrxy = corr_x_y.item(0, 1)
    corrxz = corr_x_z.item(0, 1)
    corryz = corr_y_z.item(0, 1)

    # write to csv-file.
    with open('Tot_tGrav_Freq_51.14.csv', 'a', newline='' ) as f:
        writer = csv.writer( f )
        if (i==1):
            writer.writerow(["blank", "mean-x", "mean-y", "mean-z", "std-x", "std-y", "std-z", "mad-x", "mad-y", "mad-z","max-x","max-y", "max-z", "min-x", "min-y", "min-z", "sma", "energy-x", "energy-y", "energy-z", "iqr-x", "iqr-y", "iqr-z", "entropy-x", "entropy-y", "entropy-z", "corr_coeff_X.Y", "corr_coeff_X.Z", "corr_coeff_Y.Z"])
            i = 2
        writer.writerow(["%f\r\n" % (i), (meanx), (meany), (meanz), (stdx), (stdy), (stdz), (madx), (mady), (madz), (maxx), (maxy), (maxz), (minx), (miny), (minz), (SMA), (energyx), (energyy), (energyz), (iqx), (iqy), (iqz), (entrox), (entroy), (entroz), (corrxy), (corrxz), (corryz)])
    if slider1.reached_end_of_list(): break


