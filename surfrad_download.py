import urllib.request

file_path = 'C:\\Users\\Admin\\Desktop\\' # where files will download to

first_day = 19182 # last two digits of year followed by jday (1-365)
last_day = 19244 # last two digits of year followed by jday (1-365)


station_list = ['Bondville_IL', 'Boulder_CO', 
                'Desert_Rock_NV', 'Fort_Peck_MT',
                'Goodwin_Creek_MS','Sioux_Falls_SD']

station_code_list = ['bon', 'tbl', 'dra', 'fpk', 'gwn', 'sxf']

for i in range(0,len(station_list)):
    station = station_list[i]
    station_code = station_code_list[i]

    print(f'Files Downloading: Station {i+1}/6')
    for i in range(first_day,last_day): 
        try:
            url_num = str(i)
            url = 'ftp://aftp.cmdl.noaa.gov/data/radiation/surfrad/' + station + '/2019/' + station_code + url_num + '.dat'
            file_name = file_path + station_code + url_num + '.dat'
            urllib.request.urlretrieve(url, file_name)
            
        except:
            pass

print('File download complete.')
