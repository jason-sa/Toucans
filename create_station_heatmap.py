import seaborn as sns
import pandas as pd

def create_station_heatmap(station_name, turnstile_data):
    ''' Heat map for a station by day of week and by hour
    Two heatmaps. One for Entry count and the other for Exit count
    
    station: station name for the analysis
    turnstile_data: pd.DataFrame of the MTA turnstile data. This will be the clean version that read_mta_stations()

    return (void) plot of the heat map
    '''
    # Probably turn this into a function to make it easier
    agg = turnstile_data.groupby(['STATION','DATE','TIME'])[['hourly_entries']].sum().reset_index()
    agg.DATE = pd.to_datetime(agg.DATE, format='%m/%d/%Y')
    agg.TIME = pd.to_datetime(agg.TIME, format='%H:%M:%S')
    agg['day_name'] = agg.DATE.dt.dayofweek
    agg['hour_of_day'] = agg.TIME.dt.hour
    #remove 0, 4, and 20 hours of day. Only want 8:00am, 12:00pm, and 4:00pm
    agg = agg[(agg['hour_of_day'] > 5) & (agg['hour_of_day'] < 19 )]

    
    hm = agg.loc[agg.STATION == station_name,['hour_of_day','day_name','hourly_entries']]
    hm = hm.groupby(['hour_of_day','day_name'])['hourly_entries'].mean().reset_index()
    hm = hm.pivot(index='hour_of_day',columns='day_name',values='hourly_entries')
    
    
    agg2 = turnstile_data.groupby(['STATION','DATE','TIME'])[['hourly_exits']].sum().reset_index()
    agg2.DATE = pd.to_datetime(agg2.DATE, format='%m/%d/%Y')
    agg2.TIME = pd.to_datetime(agg2.TIME, format='%H:%M:%S')
    agg2['day_name'] = agg2.DATE.dt.dayofweek
    agg2['hour_of_day'] = agg2.TIME.dt.hour
    #remove 0, 4, and 20 hours of day. Only want 8:00am, 12:00pm, and 4:00pm
    agg2 = agg2[(agg2['hour_of_day'] > 5) & (agg2['hour_of_day'] < 19 )]

    
    hm2 = agg2.loc[agg2.STATION == station_name,['hour_of_day','day_name','hourly_exits']]
    hm2 = hm2.groupby(['hour_of_day','day_name'])['hourly_exits'].mean().reset_index()
    hm2 = hm2.pivot(index='hour_of_day',columns='day_name',values='hourly_exits')

    xticks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig, ax = plt.subplots(1,2, figsize=(12, 4))
    fig.suptitle('Heatmap of Passenger Volume')
    ax[0].set_title('Entries')
    ax[1].set_title('Exits')
    sns.heatmap(hm, cmap='Blues', xticklabels=xticks, ax=ax[0])
    sns.heatmap(hm2, cmap='Blues', xticklabels=xticks, ax=ax[1])
    
    fig.show()