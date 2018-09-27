import pandas

def find_schedule(station,top_n):
    return station.stack().nlargest(top_n).reset_index()