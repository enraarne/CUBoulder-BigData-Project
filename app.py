from flask import Flask, request, render_template
from backend.data_collector.default_data import default_dates, defualt_pictures
from backend.data_collector.Yr_API import get_weather_data_from_yr
from backend.data_collector.database_connection import store_data
from backend.data_analyzer.analyze_data import analyzer

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():

    if request.method == 'POST':
        latitude = request.form.get("latitude", "")
        longitude = request.form.get("longitude", "")
    else:
        latitude = "59.9"
        longitude = "10.7"

    try:
        x_varnish, df = get_weather_data_from_yr(latitude, longitude)
        store_data(x_varnish, df)
        dates, pictures, max_value_picture, max_value_name = analyzer(x_varnish)
        coordinate_input = True
    except:
        dates, pictures = default_dates, defualt_pictures
        coordinate_input = False
    
    return render_template(
        "index.html", longitude=longitude, latitude=latitude, pictures=pictures, dates=dates, 
        coordinate_input=coordinate_input, max_value_picture=max_value_picture, max_value_name=max_value_name
    )
