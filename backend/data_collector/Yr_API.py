import requests
import pandas as pd

def get_weather_data_from_yr(lat=59.9, lon=10.7):
    """
    The function takes information about latitude and longitude and returns weather data for
    the following 7 days from Yr. 
    """
    
    endpoint = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"

    headers = {'User-Agent': 'course assignment under development arne.fevolden@yahoo.com', 
            'Accept-Encoding': 'gzip, deflate, br', 
            'Accept': '*/*', 
            'Connection': 'keep-alive'}

    response = requests.get(endpoint, headers=headers)
    

    yr_data_list = []
    for i in response.json()["properties"]['timeseries']:
        try:
            yr_data_list.append( (i['time'], i['data']['next_6_hours']['summary']['symbol_code']) ) 
        except:
            continue

            
    # Turn into DataFrame
    df = pd.DataFrame(yr_data_list, columns=['Date/time', 'Weather'])

    df['Year']  = df['Date/time'].map(lambda x: x[:4])
    df['Month'] = df['Date/time'].map(lambda x: x[5:7])
    df['Day']   = df['Date/time'].map(lambda x: x[8:10])
    df['Time']  = df['Date/time'].map(lambda x: x[11:])

    df = df[['Year', 'Month', 'Day', 'Time', 'Weather']]

    # Remove today from dataset
    today = df['Day'].iloc[0]
    mask_not_today = df['Day'] != today
    df = df[mask_not_today]
    df


    # Remove hours apart from 00, 06, 12 and 18
    mask_every_six_hours = df['Time'].isin(['00:00:00Z', '06:00:00Z', '12:00:00Z', '18:00:00Z'])
    df = df[mask_every_six_hours]

    # Remove Time
    df = df[['Year', 'Month', 'Day', 'Weather']]
    df

    # Remove data after 7 days:
    df = df.head(28)

    return response.headers['X-Varnish'] , df

