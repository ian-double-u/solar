import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import pandas as pd
import numpy as np

path_list = Path('C:\\Users\\Admin\\Desktop\\').glob('**/*.dat')
paths = []

for path in path_list:
    paths.append(str(path))
     
frames = [] # hold df for each .dat file

column_names = ['year', 'jday', 'month', 'day', 'hour', 'min', 'dt', 'zen', 
              'dw_solar', 'dw_solar_QC', 
              'uw_solar', 'uw_solar_QC',
              'direct_n', 'direct_n_QC',
              'diffuse', 'diffuse_QC',
              'dw_ir', 'dw_ir_QC',
              'dw_casetemp', 'dw_casetemp_QC',
              'dw_dometemp', 'dw_dometemp_QC',
              'uw_ir', 'uw_ir_QC',
              'uw_casetemp', 'uw_casetemp_QC',
              'uw_dometemp', 'uw_dometemp_QC',
              'uvb', 'uvb_QC',
              'par', 'par_QC',
              'netsolar', 'netsolar_QC',
              'netir', 'netir_QC',
              'totalnet', 'totalnet_QC',
              'temp', 'temp_QC',
              'rh', 'rh_QC',
              'windspd', 'windspd_QC',
              'winddir', 'winddir_QC',
              'pressure', 'pressure_QC']

for path in paths:
    print(f'Start: load file {(paths.index(path)) + 1}/{len(paths)}')

    with open(path,'r') as f:
        df = pd.DataFrame(l.rstrip().split() for l in f)
  
        station_name = df[0][0]
        lat = df[0][1]
        lng = df[1][1]
        alt = df[2][1]
        
        s = df.shape[0]-2
        df = df.tail(s).reset_index(drop=True)
        df.columns = column_names
        
        df['station_name'] = station_name
        df['lat'] = lat
        df['lng'] = lng
        df['alt'] = alt
        
        df.drop(columns=['dw_solar', 'dw_solar_QC', 
                         'uw_solar', 'uw_solar_QC',
                         'diffuse', 'diffuse_QC',
                         'dw_ir', 'dw_ir_QC',
                         'dw_casetemp', 'dw_casetemp_QC',
                         'dw_dometemp', 'dw_dometemp_QC',
                         'uw_ir', 'uw_ir_QC',
                         'uw_casetemp', 'uw_casetemp_QC',
                         'uw_dometemp', 'uw_dometemp_QC',
                         'uvb', 'uvb_QC',
                         'par', 'par_QC',
                         'netsolar', 'netsolar_QC',
                         'netir', 'netir_QC',
                         'totalnet', 'totalnet_QC',
                         'temp', 'temp_QC',
                         'rh', 'rh_QC',
                         'windspd', 'windspd_QC',
                         'winddir', 'winddir_QC',
                         'pressure', 'pressure_QC'], inplace=True)
    
    frames.append(df)
    print(f'End: load file {(paths.index(path)) + 1}/{len(paths)}')
  
print('Start: combine files.')
result = pd.concat(frames)
result.drop(result[result['direct_n_QC'] != 0].index, inplace=True) # data cleaning step
result.to_csv('surfrad_data.csv', index=False)
print('End: combine files. All .dat files now stored in surfrad_data.csv')

def return_geojson(lat,lng,increment):
    """returns geojson box around lat and lng"""

    geojson_geometry = { # (lng,lat)
    "type": "Polygon",
    "coordinates": [
    [
    [
    lng+increment,
    lat+increment
    ],
    [
    lng+increment,
    lat-increment
    ],
    [
    lng-increment,
    lat-increment
    ],
    [
    lng-increment,
    lat+increment
    ],
    [
    lng+increment,
    lat+increment
    ]
    ]
    ]
    }
    
    return geojson_geometry

stations = ['Bondville', # station names
            'Boulder', 
            'Desert Rock', 
            'Fort Peek', 
            'Goodwin Creek', 
            'Sioux Falls']

lat_lng_s = [(40.5,-88.37), # station lat/lng in order of station names
             (40.13,-105.24), 
             (36.624,-116.019), 
             (48.31,-105.1), 
             (34.25,-89.87),  
             (43.73,-96.62)]

def clouds(geojson):
    """gets cloud data from Planet API for daterange"""

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
    "gte": "2019-01-01T00:00:00.000Z", # start date of image capture
    "lte": "2019-01-02T00:00:00.000Z" # end date of image capture
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

information = [{'station': stations[i], 
                'lat': lat_lng_s[i][0], 
                'lng': lat_lng_s[i][1], 
                'geojson': return_geojson(lat_lng_s[i][0],lat_lng_s[i][1],0.03663),
                'clouds' : clouds(return_geojson(lat_lng_s[i][0],lat_lng_s[i][1],0.03663))} for i in range(0,len(stations))]


rows = []
for i in information:
    for sat in i['clouds']:
        rows.append([i['station'],sat[0],sat[1]]) # [station, clouds, time]
        
df = pd.DataFrame(rows, columns=['Station', 'Clouds (0-1)', 'Time'])
df.to_csv('clouds.csv', index=False)
print('NOAA Station cloud data stored in clouds.csv')

old_stations = ['Bondville', # station names
            'Table', # Boulder
            'Desert', # Desert Rock
            'Fort',  # Fort Peek
            'Goodwin', # Goodwin Creek
            'Sioux'] # Sioux Falls

new_stations = ['Bondville', # station names
            'Boulder', 
            'Desert Rock', 
            'Fort Peek',  
            'Goodwin Creek', 
            'Sioux Falls'] 

df1 = pd.read_csv('surfrad_data.csv')
df2 = pd.read_csv('clouds.csv')

df1['clouds'] = [np.nan]*df1.shape[0] # initalize column

# replace old stations names in df1 with new ones
for i in old_stations:
    z = list(df1.loc[df1['station_name'] == i].index)
    old_i = old_stations.index(i)
    
    for j in z:
        df1.at[j, 'station_name'] = new_stations[old_i]


# create jday column for cloud data
def get_month_days(month_number):
    """month_number = 1 in January month_number = 12 in December"""
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    return month_days[month_number-1]
        
df2['jday'] = [i for i in range(0,df2.shape[0])] # initalize column

for i in range(0,df2.shape[0]): 
    month = int(df2.loc[i]['Time'][6:7])
    day = int(df2.loc[i]['Time'][8:10])
    
    k = 0
    for j in range(1,month):
        k += get_month_days(j)
        
    df2.at[i, 'jday'] = (day + k)
    
# add all same day photos to surfrad
station_dicts = [] # list of dictionaries for each station with cloud data
    
for i in new_stations: 
    cloud_list = [] # list of dicts, one for each jday

    jj2 = list(df2.loc[df2['Station'] == i].index)

    for j in range(df2['jday'].min(),df2['jday'].max()):
        
        jj1 = list(df2.loc[df2['jday'] == j].index)
        
        jj3 = list(set(jj1) & set(jj2))
        
        try:
            day_dict = {str(j): [df2.loc[k]['Clouds (0-1)'] for k in jj3]}
            cloud_list.append(day_dict)
            
        except:
            pass
 
    cloud_dict = {'station': i, 'clouds': cloud_list}

    station_dicts.append(cloud_dict)

miss = []
for i in range(0,df1.shape[0]):
    station_index = new_stations.index(df1.loc[i]['station_name'])
    _jday = df1.loc[i]['jday']
    
    cloud_list = station_dicts[station_index]['clouds'][_jday-df2['jday'].min()][str(_jday)] 
    
    if len(cloud_list) != 0:
        df1.at[i, 'clouds'] = np.mean(cloud_list)
        
    else:
        miss.append(i)
        df1.at[i, 'clouds'] = -9999.9

# deal with missing values
df3 = df1[df1['clouds'] != -9999.9]
mean_c = np.mean(df3.clouds)
for i in miss:
    df1.at[i, 'clouds'] = mean_c

# save final file
df1.to_csv('surfrad_data.csv', index=False)
print('Final file prepared. Find surfrad_data.csv')
