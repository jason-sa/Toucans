import pandas as pd
def top_stations(station_companies, col='mean_entries', sort=False, top=5):
    df_top = pd.DataFrame(columns=station_companies.columns)
    
    groups = station_companies.groupby(['COMPANY'])
    for name, group in groups:
        if sort:
            df_top = df_top.append(group.nsmallest(top, col))
        else:
            df_top = df_top.append(group.nlargest(top, col))
    return df_top