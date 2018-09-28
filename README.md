# Project
First project from Metis Fall 2018 Bootcamp (Project Benson) with Dana Lindquist, Jason Salazer-Adamso Leo Liu & Spencer Tollefson
 
# Flow of Data Analysis
* [Presentation](/Toucans_Presentation.pdf)

# Description of Functions

* `find_schedule` - 
* `merge_station_company` - Function to merge MTA station master data with Grace Hopper company master data and calculate distance between station to company.
* `read_mta_stations` - 
* `read_mta_turnstile` - Reads the MTA turnstile data from http://web.mta.info/developers/turnstile.html for a given date range and creates a data frame.
* `read_tech_compaines` -
* `top_stations` - Calculates the top station/company pairs based on a column in a merge station_company data frame.
* `create_station_heatmap` - This function inputs a **Name** of a MTA station and a **DataFrame** with complete, clean MTA turnstile count data. It outputs two heatmaps - one for Entries and one for Exits - that shows the highest conentrated passenger throughput by time of day (morning, midday, evening) and day of week.

# Explanation of Standard Libraries
* `from geopy.distance import geodesic` - Library to calculate the distance between to points with Lat/Long coordinates
* `from mpl_toolkits.basemap import Basemap` - Library to plot maps and points on the maps
* 

# Data sources
* MTA Turnstile Data - http://web.mta.info/developers/turnstile.html
* MTA Station Data - https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49 (export data as csv)
* Grace Hopper Companies - https://ghc.anitab.org/2017-sponsorships/corporate-sponsors/ [tech_companies.csv](data/tech_companies.csv)

