# Flow of Data Analysis
* [Presentation](/Toucans_Presentation.pdf)

# Description of Functions
* `create_station_heatmap` - This function inputs a **Name** of a MTA station and a **DataFrame** with cleaned MTA data of the station passenger count of  Entries and Exits per day. It outputs two heatmaps - one for Entries and one for Exits - that shows the highest conentrated passenger throughput by time of day (morning, midday, evening) and day of week.
* `find_schedule` - 
* `merge_station_company` - Function to merge MTA station master data with Grace Hopper company master data and calculate distance between station to company.
* `read_mta_stations` - 
* `read_mta_turnstile` - Reads the MTA turnstile data from http://web.mta.info/developers/turnstile.html for a given date range and creates a data frame.
* `read_tech_compaines` -
* `top_stations` - Calculates the top station/company pairs based on a column in a merge station_company data frame.

# Explanation of Standard Libraries
* `from geopy.distance import geodesic` - Library to calculate the distance between to points with Lat/Long coordinates
* 

# Data sources
* MTA Turnstile Data - http://web.mta.info/developers/turnstile.html
* MTA Station Data - https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49 (export data as csv)
* Grace Hopper Companies - [tech_companies.csv](data/tech_companies.csv)

