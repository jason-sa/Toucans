import numpy as np
from geopy.distance import geodesic
import pandas as pd

def merge_station_company(stations, companies, turnstiles):
    
    # cross join the two data frames
    stations['_tmpkey'] = 1
    companies['_tmpkey'] = 1
    station_companies = pd.merge(companies, stations, how='outer', on='_tmpkey').drop('_tmpkey', axis=1)
    
    # remove rd, th, and st to match stations with the turnstile data
    station_companies.name = station_companies.name.str.replace('rd ',' ')
    station_companies.name = station_companies.name.str.replace('th ',' ')
    station_companies.name = station_companies.name.str.replace('st ',' ')
    station_companies.name = station_companies.name.str.replace('1 Ave', '1 AV')
    
    # set station as the index for joining
    station_companies.rename(columns={'name':'STATION'}, inplace=True)
    station_companies.STATION = station_companies.STATION.str.upper()
    station_companies.index = station_companies.STATION
    station_companies.rename(columns={'STATION':'STAION_nm'}, inplace=True)
    
    # calculate distance
    station_companies['distance'] = np.nan
    station_companies['comp_lat_lon'] = list(zip(station_companies.LAT, station_companies.LON))
    station_companies['station_lat_lon'] = list(zip(station_companies.lat, station_companies.lon))
    station_companies['distance'] = [geodesic(v, station_companies.iloc[k,10]).miles for k, v in enumerate(station_companies.comp_lat_lon)]
    
    # calculate mean / max stats by station
    station_hour_day = turnstiles.groupby(['STATION','DATE','hour'])['hourly_entries'].sum()
    station_mean = station_hour_day.groupby('STATION').mean()
    station_max = station_hour_day.groupby('STATION').max()

    # be aware of data errors -- need to determine if further cleaning is needed. (2996/6622)
    station_companies = station_companies.join(station_mean, how='inner')
    station_companies.rename(columns={'hourly_entries':'mean_entries'}, inplace=True)

    station_companies = station_companies.join(station_max, how='inner')
    station_companies.rename(columns={'hourly_entries':'max_entries'}, inplace=True)
    

    return station_companies