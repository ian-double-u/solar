"""Basic intro. plotting for pyranometer data"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

tau = 2*np.pi

file_list = ['june_26_2020_UTCstart_20_25_00_timesadded',
             'june_27_2020_UTCstart_02_44_00_timesadded',
             'june_27_2020_UTCstart_08_49_00_timesadded',
             'june_28_2020_UTCstart_00_50_00_timesadded',
             'june_29_2020_UTCstart_19_15_00_timesadded',
             'june_30_2020_UTCstart_16_00_00_timesadded',
             'july_01_2020_UTCstart_14_32_00_timesadded',
             'july_02_2020_UTCstart_17_47_00_timesadded']

for file in file_list:
    df = pd.read_csv(file + '.csv')

    x = []
    y = []
    day_orig = df['PST'].loc[0][-11:-9]
    if (day_orig[0] != '0'):
            day_orig = int(day_orig)
    else:
        day_orig = int(day_orig[1])
    
    for i in range(0,df.shape[0]):
        # Get hour, minute and seconds 
        ### > > > ASSUMES proper format and '_timesadded' < < < ###
        day = df['PST'].loc[i][-11:-9]
        if (day[0] != '0'):
            day = int(day)
        else:
            day = int(day[1])
        
        hour = df['PST'].loc[i][-8:-6]
        if (hour[0] != '0'):
            hour = int(hour)
        else:
            hour = int(hour[1])
        
        minute = df['PST'].loc[i][-5:-3]
        if (minute[0] != '0'):
            minute = int(minute)
        else:
            minute = int(minute[1])
            
        second = df['PST'].loc[i][-2:]
        if (second[0] != '0'):
            second = int(second)
        else:
            second = int(second[1])
            
        if (day > day_orig):
            hour += 24
            
        x.append(hour + minute/60 + second/3600)
        y.append(df['Data Set 1:Irradiance(W/m²)'].loc[i])
       
    # Plot Pyranometer data
    plt.subplot(1,2,1)
    plt.plot(x,y, color='#FF7951')
    plt.title(f'Observed Solar Irradiance\n', fontsize=16)
    plt.xlabel('24-Hour Local Time (PST), ', fontsize=14)
    plt.ylabel('Irradiance (W/m2)', fontsize=14)
    plt.ylim(0,1300)
    plt.tight_layout()
    
    # Plot LS-Regression of Sin function on Data
    x = np.asarray(x)
    y = np.asarray(y)
    
    guess_mean = np.mean(y)
    guess_phase = x[0]
    guess_freq = (x[-1]-x[0])/tau
    guess_amp = np.mean(y)
    
    data_first_guess = guess_amp*np.sin(guess_freq*y + guess_phase) + guess_mean
    
    optimize_func = lambda t: t[0]*np.sin(t[1]*x + t[2]) + t[3] - y
    est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [guess_amp, guess_freq, guess_phase, guess_mean], maxfev=5000)[0]
    
    # recreate the fitted curve using the optimized parameters
    data_fit = est_amp*np.sin(est_freq*x + est_phase) + est_mean
    
    # recreate the fitted curve using the optimized parameters
    fine_x = np.arange(x[0],x[-1],0.1)
    data_fit=est_amp*np.sin(est_freq*fine_x + est_phase) + est_mean
    
    # Calculate MSE
    n = len(data_fit)
    sum = 0
    
    for i in range(0,n):
      sum += (data_fit[i]-y[i])**2
    
    MSE = sum/n
    
    plt.subplot(1,2,2)
    plt.plot(x, y, '.', color='#FF7951')
    plt.plot(fine_x, data_fit, color='b')
    plt.title(f'Least Squares Fitting\nMSE = {MSE:.2f}', fontsize=16)
    plt.xlabel(f'Mean Julian Day {df["JD"].mean():.2f}', fontsize=14)
    plt.ylim(0,1300)
    plt.tight_layout()
    plt.show()
    plt.close()
