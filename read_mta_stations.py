def read_mta_stations():
    ''' Read the MTA master list into a pd.DataFrame (Put the CSV file on the repository!!)
    data source = ttps://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49 (export data as csv)

    return pd.DataFrame (columns = [station (unique), lattitude, longitude])
    '''