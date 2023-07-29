import pandas as pd
from tinydb import TinyDB, Query

def store_data(x_varnish, df):

    dates = [f"{df['Month'].iloc[i]}-{df['Day'].iloc[i]}-{df['Year'].iloc[i]}" for i in range(0, 28, 4)]

    # Database entry
    db = TinyDB('backend/weather_db')
    if len(db) > 1000:
        db.truncate()
    db.insert({'x_varnish': x_varnish, 'dates': dates, 'weather': df['Weather'].tolist()})


