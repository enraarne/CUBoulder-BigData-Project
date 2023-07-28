import pandas as pd
from tinydb import TinyDB, Query
from backend.data_analyzer.weather_data_categories import transformation_dict

def analyzer(x_varnish):
    
    db = TinyDB('backend/weather_db')
    User = Query()

    result = db.search(User.x_varnish == x_varnish)[0]

    # producing dates for the frontend
    dates = result['dates']
    
    # producing pictures for the frontend
    pictures = [str(i) + '.svg' for i in result['weather']]

    # finding the picture of the most common weather condition for the frontend
    count={}
    for c in pictures:
        count[c]=count.setdefault(c, 0)+1
    max_value_picture = max(count, key=count.get)
    
    # finding the name of the most common weather condition for the frontend
    names = [str(i) for i in result['weather']]
    
    count={}
    for c in names:
        count[c]=count.setdefault(c, 0)+1
    max_value_name = max(count, key=count.get)
    max_value_name = transformation_dict[max_value_name]

    return dates, pictures, max_value_picture, max_value_name
