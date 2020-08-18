# MLR Model

# Libraries
import pandas as pd
import random as r
import numpy as np
from sklearn import linear_model
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_squared_error

# Read and Prepare Data
df = pd.read_csv('surfrad_data.csv') 
anomaly = list(df[df['direct_n_QC'] != 0].index)
df.drop(anomaly, axis=0, inplace=True) # incorrect measurements

df2 = pd.read_csv('my_data.csv') 

# Create Train/Test Split
sort = [r.random() for i in range(0,df.shape[0])]
df['sort'] = sort
df.sort_values('sort', inplace=True)

u = int(0.8*df.shape[0])
v = df.shape[0] - u

df_train = df.head(u)
df_test = df.tail(v)

# Build Model
regr = linear_model.LinearRegression()
x = np.asanyarray(df_train[['jday','dt','zen', 'lat', 'lng', 'clouds']])
y = np.asanyarray(df_train[['direct_n']])
regr.fit(x, y)


print('Multiple Linear Regression\n')
print('Test Set;')
print('Coefficients: ', regr.coef_)
print('Intercept: ', regr.intercept_)

y_hat = regr.predict(df_test[['jday','dt','zen', 'lat', 'lng', 'clouds']])
y = np.asanyarray(df_test[['direct_n']])

### MSE
print(f'\nMSE: {mean_squared_error(y,y_hat):.2f}')

### Explained variance 
print(f'Explained varirance: {explained_variance_score(y,y_hat):.2f}\n')

### Retrain on all of surfrad_data.csv and test on my_data.csv
print('My Data;')

regr = linear_model.LinearRegression()

x = np.asanyarray(df[['jday','dt','zen', 'lat', 'lng', 'clouds']])
y = np.asanyarray(df[['direct_n']])
regr.fit(x, y)

print('Coefficients: ', regr.coef_)
print('Intercept: ', regr.intercept_)

y_hat = regr.predict(df2[['jday','dt','zen', 'lat', 'lng', 'clouds']])
y = np.asanyarray(df2[['direct_n']])

### MSE
print(f'\nMSE: {mean_squared_error(y,y_hat):.2f}')

### Explained variance
print(f'Explained varirance: {explained_variance_score(y,y_hat):.2f}')

"""
Results:

Multiple Linear Regression

Test Set;
Coefficients:  [[   0.74346125    3.78480819   -6.89432717   -5.3114602    -4.61535721
  -263.69513733]]
Intercept:  [402.14996274]

MSE: 61893.76
Explained varirance: 0.54 # not bad given the simplicity of the model

My Data;
Coefficients:  [[   0.76532176    3.84793281   -6.89149404   -5.31592378   -4.63139446
  -264.79769713]]
Intercept:  [395.55562318]

MSE: 101870.75
Explained varirance: -0.06 # i.e. worse than a horizontal line
"""
