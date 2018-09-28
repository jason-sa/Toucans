import pandas as pd
def top_stations(station_companies, col='mean_entries', sort=False, top=5):
    ''' Calculates the top station company pairing based on given col, sort criteria, 
        and number of records to return.

        station_companies = df of merge company and station data
        col = column in the data frame to perform the top n analysis
        sort = True:Descending, False:Ascending
        top = top n rows of data

        return pd.DataFrame subset of station_companie and filterd to top n
    '''
    df_top = pd.DataFrame(columns=station_companies.columns)
    
    groups = station_companies.groupby(['COMPANY'])
    for name, group in groups:
        if sort:
            df_top = df_top.append(group.nsmallest(top, col))
        else:
            df_top = df_top.append(group.nlargest(top, col))
            
    return df_top