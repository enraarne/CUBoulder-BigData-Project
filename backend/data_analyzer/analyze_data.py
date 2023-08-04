import pandas as pd
from tinydb import TinyDB, Query
from backend.data_analyzer.weather_data_categories import transformation_dict

def analyzer(data, stand_alone_program=False):
    """
    To use the analyzer as a stand alone program, set stand_alone_program to True. The data must be provided
    as a dictionary with the following format:

    data = {
    "dates": ["07-28-2023", "07-29-2023", "07-30-2023", "07-31-2023", "08-01-2023", "08-02-2023", "08-03-2023"], 
    "weather": ["cloudy", "rainshowers_day", "fair_day", "fair_night", "cloudy", "partlycloudy_day", "partlycloudy_day", "cloudy", "cloudy", "rain", "rain", "cloudy", "cloudy", "rain", "rain", "cloudy", "rain", "cloudy", "rain", "cloudy", "cloudy", "rainshowers_day", "rain", "cloudy", "partlycloudy_night", "cloudy", "cloudy", "partlycloudy_night"]
    }

    Otherwise, the program will use the the data as x_varnish values for fetching information from the database 
    """

    if stand_alone_program == False:
        db = TinyDB('backend/weather_db')
        User = Query()

        result = db.search(User.x_varnish == data)[0]
    else:
        result = data

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
