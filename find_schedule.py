import pandas

# This function takes in a station's turnstile data as a DataFrame
# called "station" and an integer which specifies the number of largest 
# value to be returned.
def find_schedule(station,top_n):
    return station.stack().nlargest(top_n).reset_index()