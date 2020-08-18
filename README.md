# solar

## solar irradiance prediction project


### Overview


### Data
See the [data folder](https://github.com/ian-double-u/solar/tree/master/data) to view the data I used and see [instructions.md](https://github.com/ian-double-u/solar/blob/master/data/instructions.md) to learn how to put it together yourself; including collecting your own solar irradiance data with [Vernier Sensors]([https://www.vernier.com/](https://www.vernier.com/)).


The data used in this project comes from two sources. NOAA's SURFRAD project and data collected personally. However, if you do not have access to the required hardware you can use SURFRAD data exclusively. 


The SURFRAD data is collected at 6 separate sites across the United States with very high fidelity (1 observation/minute). The geographic variety and vast quantity of data (going back many years) makes it perfect for training models.

In this project I use the SURFRAD data to train my model(s) and then use the irradiance data I collected myself as a test set.


### Modeling


If you are interested in experimenting with your own models you can use the below code to pre-process all of the data and insert your own model. This template can also be found [here](https://github.com/ian-double-u/solar/blob/master/model_template.py)
```python
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

```


Otherwise, I provide some examples of models you *could* build to try and predict the irradiance data you observed. 
