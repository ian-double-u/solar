import pandas as pd
import numpy as np
import os
import requests
from requests.auth import HTTPBasicAuth

files = [] # list of all file names (no .csv at end)

time_zone = 'UTC' # timezone of collection point
local_lat = 1.00001 # lattitude of collection point
local_lng = 1.00001 # longitude of collection point

geo_json = {} # geo_json object of collection point
 
df = pd.concat([pd.read_csv(file + '.csv') for file in files], ignore_index=True)
df.rename(columns={'Data Set 1:Irradiance(W/m²)': 'direct_n'}, inplace=True)
df.drop(columns=['Data Set 1:Time(s)'], axis=1, inplace=True)

# Add jday column
df['jday'] = [0.0]*df.shape[0]

def get_month_days(month_number):
    """month_number = 1 in January month_number = 12 in December"""
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    return month_days[month_number-1]

for i in range(0,df.shape[0]):
    month = int(df.loc[i][time_zone][5:7])
    day = int(df.loc[i][time_zone][8:10])
    
    jday = 0
    
    for j in range(1,month):
        jday += get_month_days(j)
        
    jday += day
    
    df.at[i, 'jday'] = jday

# Add dt column
df['dt'] = [0.0]*df.shape[0]

for i in range(0,df.shape[0]):
    hour = float(df.loc[i][time_zone][11:13])/24 
    min_ = float(df.loc[i][time_zone][14:16])/1440
    sec = float(df.loc[i][time_zone][17:19])/86400
    
    dt = (hour + min_ + sec)*24.0

    df.at[i, 'dt'] = dt
    
# Add lat and lng columns
df['lat'] = local_lat
df['lng'] = local_lng

# Add zen
df['zen'] = [0.0]*df.shape[0]

for i in range(0,df.shape[0]):
    day = df.loc[i]['jday']
    lat = 45.4612
    
    hour = float(df.loc[i][time_zone][11:13])
    min_ = float(df.loc[i][time_zone][14:16])
    sec = float(df.loc[i][time_zone][17:19])

    day_angle = (np.pi*2*(day))/365
    declination = (180/np.pi)*(0.006918 - 0.399912*np.cos(day_angle)
                               + 0.070257*np.sin(day_angle)
                               - 0.006758*np.cos(2*day_angle)
                               + 0.000907*np.sin(2*day_angle)
                               - 0.002697*np.cos(3*day_angle)
                               + 0.00148*np.sin(3*day_angle))
    
    declination = (declination*np.pi)/180
    
    hour_angle = 0
    
    if hour == 12:
        hour_angle = (min_/60 + sec/360)*15
    
    elif hour < 12:
        hour_angle = ((12-hour) + min_/60 + sec/360)*-15
    
    else: # hour > 12
        hour_angle = ((hour-12) + min_/60 + sec/360)*15
        
    zen = np.arccos(np.sin(lat)*np.sin(declination) + 
                    np.cos(lat)*np.cos(declination)*np.cos(hour_angle))    
    
    df.at[i, 'zen'] = (zen*180)/np.pi
    
# Add clouds
def clouds(geojson):
    """gets cloud data from Planet API for date range"""

    geojson_geometry = geojson # takes lng/lat
    
    geometry_filter = {
    "type": "GeometryFilter",
    "field_name": "geometry",
    "config": geojson_geometry
    }
    
    date_range_filter = { 
    "type": "DateRangeFilter",
    "field_name": "acquired",
    "config": {
    "gte": "2020-01-01T00:00:00.000Z", # start date of image capture
    "lte": "2020-01-02T00:00:00.000Z" # end date of image capture
    }
    }
    
    combined_filter = {
    "type": "AndFilter",
    "config": [geometry_filter, date_range_filter]
    }
    
    os.environ['PL_API_KEY']='' # insert planet API key
    PLANET_API_KEY = os.getenv('PL_API_KEY')
    
    search_request = {
    "item_types": ["PSScene4Band"],
    "filter": combined_filter
    }
    
    search_result = \
      requests.post(
        'https://api.planet.com/data/v1/quick-search',
        auth=HTTPBasicAuth(PLANET_API_KEY, ''),
        json=search_request)
    
    cloud_date = [(feature['properties']['cloud_cover'],feature['properties']['acquired']) for feature in search_result.json()['features']]
    
    return cloud_date

clouds = clouds(geo_json)

df['clouds'] = [0.0]*df.shape[0]

for i in range(0,df.shape[0]):
    month = int(df.loc[i][time_zone][5:7])
    day = int(df.loc[i][time_zone][8:10])
    
    cloud_list = [t[0] for t in clouds if int(t[1][5:7]) == month and int(t[1][8:10]) == day]
    
    if len(cloud_list) == 0:
        df.at[i, 'clouds'] = -9999.9
        
    else:
        df.at[i, 'clouds'] = np.mean(cloud_list)
        
avg_clouds = np.mean(df[df['clouds'] != -9999.9]['clouds'])
    
for i in range(0,df.shape[0]):
    if df.loc[i]['clouds'] == -9999.9:
        df.at[i, 'clouds'] = avg_clouds

# Save file
df.to_csv('my_data.csv', index=False)
