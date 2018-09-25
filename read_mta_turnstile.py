def read_mta_turnstile(start, end):
    ''' Read MTA turnstile data. Clean bad data. 

    start = start date for analysis in yyymmdd format
    end = end date for analysis in yyymmmdd format

    return pd.DataFrame (list of columns + entries and exits summarized)
    '''