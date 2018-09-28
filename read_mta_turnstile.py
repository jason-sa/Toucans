import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta

def mta_end_of_week(d):
    ''' Calculates the end of the week for a given date to conform to MTA data publication on Saturday
        
        d = date vaule
        return: date 
    '''
    return d - timedelta(days=d.weekday()) + timedelta(days=5)

def read_mta_turnstile(start='20180501', end='20180531'):
    ''' Read MTA turnstile data. Calculates 4-hour bucket entries and exits for each (C/A, UNIT, SCP, STATION)

    start = start date for analysis in yyymmdd format
    end = end date for analysis in yyymmmdd format

    return pd.DataFrame (same list of columns as in the MTA CSV +
                        [date_time, entries_offset, exits_offset, hourly_entries, hourly_exits])
    '''
    first = mta_end_of_week(datetime.strptime(start, '%Y%m%d').date())
    last = mta_end_of_week(datetime.strptime(end, '%Y%m%d').date())
    
    url = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
    
    df = pd.DataFrame(columns=['C/A','UNIT','SCP','STATION','LINENAME','DIVISION','DATE','TIME','DESC','ENTRIES','EXITS'])
    while first <= last:
        data_file = url + datetime.strftime(first,'%y%m%d') + '.txt'
        print('Reading:', data_file)
        df = df.append(pd.read_csv(data_file), sort=False)
        first = first + timedelta(weeks=1)
    
    # fix some weird column thing where EXISTS is name with whitespace
    df.iloc[:,10] = df.iloc[:,11]
    df = df.iloc[:,:11]
    df.rename(columns={'C/A':'CA'}, inplace=True) # rename column for easier (dot) access

    # group df into (CA, UNIT, SCP, STATION)
    df['date_time'] = pd.to_datetime(df.DATE + ' ' + df.TIME, format='%m/%d/%Y %H:%M:%S')
    df['hour'] = df.date_time.dt.hour
    df.sort_values(by=['STATION','CA','UNIT','SCP','date_time'], inplace=True)
    df['entries_offset'] = df.groupby(['CA','UNIT','SCP','STATION'])['ENTRIES'].shift(-1) # get everything one row down and shift up
    df['exits_offset'] = df.groupby(['CA','UNIT','SCP','STATION'])['EXITS'].shift(-1)
    df['hourly_entries'] = df.entries_offset - df.ENTRIES
    df['hourly_exits'] = df.exits_offset - df.EXITS

    # set all hourly entires < 0 to negative
    df.loc[df.hourly_entries < 0,'hourly_entries'] = np.nan
    df.loc[df.hourly_exits < 0,'hourly_exits'] = np.nan
    df.loc[df.hourly_entries > 100000,'hourly_entries'] = np.nan
    df.loc[df.hourly_exits > 100000,'hourly_exits'] = np.nan

    # set entries data to floats
    df.hourly_entries = df.hourly_entries.astype(float)
    df.hourly_exits = df.hourly_exits.astype(float)
    
    # reset the indicies as they repeat for each download
    df.reset_index(inplace=True)
    return df

'''
# example usage
mta = read_mta_turnstile()
#mta = read_mta_turnstile('20180501','20180508')
print(mta.info())
'''