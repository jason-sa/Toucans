import pandas as pd
def read_tech_companies():
    ''' Data frame of 10 tech companies

    return pd.DataFrame(tech_company_name, lattitude, longitude)
    '''
    companies = pd.read_csv("data/tech_companies.csv")
    companies.drop(['ADDRESS'], axis=1, inplace=True)
    
    return(companies)
