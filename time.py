from datetime import datetime
import pandas as pd

# Data file name
file = 'FILE_NAME.csv'

# Local timezone name
time_zone = 'UTC'

# Start time of data collection (Local Time)
year_ = 2020
month_ = 1
day_ = 1
hour_ = 10
minute_ = 10
second_ = 10
collection_start = datetime(year_,month_,day_,hour_, minute_,second_,0)

interval = 1 # number of samples collected / minute (1 =< interval =< 60)

df = pd.read_csv(file)
df[time_zone].loc[0] = collection_start
samples = df.shape[0] # number of samples collected over collection period

def get_month_days(month_number):
    """month_number = 1 in January month_number = 12 in December"""
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    return month_days[month_number-1]

def time_adjust(time,interval):
    """takes initial datetime object and 
    returns a new one one interval later"""
    
    old_time = time
    old_year = old_time.year
    old_month = old_time.month
    old_day = old_time.day
    old_hour = old_time.hour
    old_minute = old_time.minute
    
    month_length = get_month_days(old_month)
    
    if ((old_minute + interval) < 60): 
        new_time = old_time.replace(minute=(old_minute + interval))
        return new_time # if interval does not change hour
    
    else:
        new_minute = (old_minute + interval)%60
        
        if ((old_hour + 1) < 24):
            new_time = old_time.replace(hour=(old_hour + 1),minute=(new_minute))
            return new_time # if interval changes hour but not day
        
        else:
            new_hour = (old_hour + 1)%24
            
            if ((old_day + 1) < (month_length+1)):
                new_time = old_time.replace(day=(old_day + 1),hour=new_hour,minute=new_minute)
                return new_time # if interval changes hour and day but not month
            
            else:
                new_day = (old_day + 1)%(month_length+1)
                
                if ((old_month + 1) < 13):
                    new_time = old_time.replace(month=(old_month + 1),day=new_day,hour=new_hour,minute=new_minute)
                    return new_time # if interval changes hour, day and month but not year
                
                else:
                    new_month = (old_month + 1)%13
                    new_time = old_time.replace(year=(old_year + 1),month=new_month,day=new_day,hour=new_hour,minute=new_minute)
                    return new_time
                
# Add times to Local time column (Local Time of each observation)
for i in range(1,samples + 1):
    df[time_zone].loc[i] = time_adjust(df[time_zone].loc[i-1],interval)
    
# Save file
df.to_csv(file,index=False)
