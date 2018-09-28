import numpy as np
from geopy.distance import geodesic
import pandas as pd

def merge_station_company(stations, companies, turnstiles, thresh=0.25):
    ''' Merges station and company dataframes into a single data frame. Calcualtes mean/max entries
        from turnstile data. Filters the merged data frame to stations within a radius of thresh.

        stations = df of MTA stations
        companies = df of Grace Harper companies
        turnstiles = df of MTA turnstile data over time

        returns pd.DataFrame of the merged station/company data
    '''
    # agg to station level taking the min lat/long
    station_agg = stations.groupby('name').min().reset_index()[['name','lon','lat']]

    # cross join the two data frames
    station_agg['_tmpkey'] = 1
    companies['_tmpkey'] = 1
    station_companies = pd.merge(companies, station_agg, how='outer', on='_tmpkey').drop('_tmpkey', axis=1)
    
    # remove rd, th, and st to match stations with the turnstile data
    station_companies.name = station_companies.name.str.replace('rd ',' ')
    station_companies.name = station_companies.name.str.replace('th ',' ')
    station_companies.name = station_companies.name.str.replace('st ',' ')
    station_companies.name = station_companies.name.str.replace('1 Ave', '1 AV')
    station_companies.name = station_companies.name.str.upper()

    #station clean-up
    station_companies.name = station_companies.name.str.replace('47TH-50 STS - ROCKEFELLER CTR', '47-50 STS ROCK')
    station_companies.name = station_companies.name.str.replace('5 AVE - 53 ST', '5 AV/53 ST')
    station_companies.name = station_companies.name.str.replace('5 AVE - 59 ST', '5 AV/59 ST')
    station_companies.name = station_companies.name.str.replace('59 ST - COLUMBUS CIRCLE', '59 ST COLUMBUS')
    station_companies.name = station_companies.name.str.replace('BROADWAY - LAFAYETTE ST', 'B\'WAY-LAFAYETTE')
    station_companies.name = station_companies.name.str.replace('CANAL ST - HOLLAND TUNNEL', 'CANAL ST')
    station_companies.name = station_companies.name.str.replace('34 ST - HUDSON YARDS', '34 ST-HUDSON YD')
    station_companies.name = station_companies.name.str.replace('34 ST - PENN STATION', '34 ST-PENN STA')
    station_companies.name = station_companies.name.str.replace('42ND ST - BRYANT PK', '42 ST-BRYANT PK')
    station_companies.name = station_companies.name.str.replace('42ND ST - PORT AUTHORITY BUS TERM', '42 ST-PORT AUTH')
    station_companies.name = station_companies.name.str.replace('5 AVE - BRYANT PK', '42 ST-BRYANT PK') # next closest to 5th/bryant prk
    station_companies.name = station_companies.name.str.replace('HERALD SQ - 34 ST', '34 ST-HERALD SQ')
    station_companies.name = station_companies.name.str.replace('TIMES SQ - 42ND ST', 'TIMES SQ-42 ST')
    station_companies.name = station_companies.name.str.replace('GRAND CENTRAL - 42ND ST', 'GRD CNTRL-42 ST')
    station_companies.name = station_companies.name.str.replace('LEXINGTON AVE - 53 ST', 'LEXINGTON AV/53')
    station_companies.name = station_companies.name.str.replace('6 AVE', '6 AV')
    station_companies.name = station_companies.name.str.replace('UNION SQ - 14 ST', '14 ST-UNION SQ')
    station_companies.name = station_companies.name.str.replace('3 AVE', '3 AV')
    station_companies.name = station_companies.name.str.replace('8 ST - NYU', '8 ST-NYU')
    station_companies.name = station_companies.name.str.replace('W 4 ST - WASHINGTON SQ (LOWER)	', 'W 4 ST-WASH SQ')
     
    # calculate distance
    station_companies['distance'] = np.nan
    station_companies['comp_lat_lon'] = list(zip(station_companies.LAT, station_companies.LON))
    station_companies['station_lat_lon'] = list(zip(station_companies.lat, station_companies.lon))
    station_companies['distance'] = [geodesic(v, station_companies.iloc[k,8]).miles for k, v in enumerate(station_companies.comp_lat_lon)]
    station_companies = station_companies[station_companies.distance <= thresh]
    
    # calculate mean / max stats by station
    station_hour_day = turnstiles.groupby(['STATION','DATE','hour'])['hourly_entries'].sum()
    station_mean = station_hour_day.groupby('STATION').mean().reset_index()
    station_max = station_hour_day.groupby('STATION').max().reset_index()

    # Join the mean / max statistics to the station_company merged df.
    station_companies = station_companies.merge(station_mean, left_on='name', right_on='STATION', how='left')
    station_companies.rename(columns={'hourly_entries':'mean_entries'}, inplace=True)

    station_companies = station_companies.merge(station_max, left_on='name',right_on='STATION', how='left')
    station_companies.rename(columns={'hourly_entries':'max_entries'}, inplace=True)
    

    return station_companies