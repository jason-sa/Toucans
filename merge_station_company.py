import numpy as np
import pandas as pd
from geopy.distance import geodesic

def create_station_company(stations, companies):
    stations['_tmpkey'] = 1
    companies['_tmpkey'] = 1
    station_companies = pd.merge(companies, stations, how='outer', on='_tmpkey').drop('_tmpkey', axis=1)
    station_companies['distance'] = np.nan
    
    station_companies['comp_lat_lon'] = list(zip(station_companies.LAT, station_companies.LON))
    station_companies['station_lat_lon'] = list(zip(station_companies.lat, station_companies.lon))
    station_companies['distance'] = [geodesic(v, station_companies.iloc[k,10]).miles for k, v in enumerate(station_companies.comp_lat_lon)]

    return station_companies