import numpy as np
import pandas as pd


def read_mta_stations():
    ''' Read the MTA master list into a pd.DataFrame (Put the CSV file on the repository!!)
    data source = https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49 (export data as csv)
    '''
    df = pd.read_csv("data/mta_stations.csv")
    df.rename(columns = {"OBJECTID": "key", "NAME":"name", "the_geom":"location"}, inplace = True)
    
    # Parsing the location data into two separate columns "lat" and "lon"
    df["lon"] = df.location.str.split().str.get(1).str.strip('(')
    df["lat"] = df.location.str.split().str.get(2).str.strip(')')
    df = df[["key","name","LINE","lon","lat"]]
    df = df.sort_values(["name","LINE"], ascending = [True, True])
    
    return df
    
    '''
    return pd.DataFrame (columns = [station (unique), lattitude, longitude])
    '''