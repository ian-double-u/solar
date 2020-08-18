import pandas as pd
import random as r
import numpy as np

# Read and Prepare Data
df1 = pd.read_csv('surfrad_data.csv') 
anomaly = list(df[df['direct_n_QC'] != 0].index)
df.drop(anomaly, axis=0, inplace=True) # drop incorrect measurements

df2 = pd.read_csv('my_data.csv') 

# Create Train/Test Split
sort = [r.random() for i in range(0,df.shape[0])]
df['sort'] = sort
df.sort_values('sort', inplace=True)

u = int(0.8*df.shape[0])
v = df.shape[0] - u

df_train = df.head(u)
df_test = df.tail(v)

# # # # # # # # # # # # # #  

# INSERT YOUR MODEL HERE #

# # # # # # # # # # # # # #
