import unittest
from tinydb import TinyDB, Query

from backend.data_analyzer.weather_data_categories import transformation_dict
from backend.data_collector.default_data import default_dates, defualt_pictures
from backend.data_collector.Yr_API import get_weather_data_from_yr
from backend.data_analyzer.analyze_data import analyzer


class Apptester(unittest.TestCase):
    
    # Unit test transformation_dict
    def test_transformation_dict(self):
        self.assertEqual(transformation_dict['rainshowers_day'], 'rain showers')
        self.assertEqual(transformation_dict['clearsky_day'], 'clear sky')
        #print("unit_test_transformation_dict: OK")
    
    
    # Unit test default data
    def test_default_data(self):
        
        default_dates_correct = ['XX-XX-XXXX', 'XX-XX-XXXX', 'XX-XX-XXXX', 'XX-XX-XXXX', 'XX-XX-XXXX', 
                         'XX-XX-XXXX', 'XX-XX-XXXX']

        defualt_pictures_correct = ['snowshowersandthunder_day.svg'] * 28
    
        self.assertEqual(default_dates, default_dates_correct)
        self.assertEqual(defualt_pictures, defualt_pictures_correct)
        #print("unit_test_default_data: OK")
    
    
    # Integration test API
    def test_API(self):
        x_varnish, df = get_weather_data_from_yr()
        self.assertGreater(len(x_varnish), 1)
        self.assertEqual(len(df), 28)
        #print("integration_test_API: OK")
        
    
    # Integration test Database
    def test_db(self):
        
        x_varnish = 123
        dates     = ['07-28-2023', '07-29-2023', '07-30-2023']
        weather   = ['cloudy', 'cloudy', 'cloudy']
        
        # instanciate db
        db = TinyDB('backend/weather_db') #'backend/weather_db'
        User = Query()
        
        # insert row
        db.insert({'x_varnish': x_varnish, 'dates': dates, 'weather': weather})
        
        # fetch entry
        result = db.search(User.x_varnish == x_varnish)[0]
        
        # remove entry
        db.remove(User.x_varnish == 123)
        
        # Test
        self.assertEqual(result['x_varnish'], 123)
        self.assertEqual(result['dates'], ['07-28-2023', '07-29-2023', '07-30-2023'])
        self.assertEqual(result['weather'], ['cloudy', 'cloudy', 'cloudy'])
        
        #print("integration_test_db: OK")
    
    
    # Integration test Analyzer
    def test_analyzer(self):
        
        x_varnish = 123
        dates     = ['07-28-2023', '07-29-2023', '07-30-2023']
        weather   = ['cloudy', 'cloudy', 'cloudy']
        
        # instanciate db
        db = TinyDB('backend/weather_db') #'backend/weather_db'
        User = Query()
        
        # insert row
        db.insert({'x_varnish': x_varnish, 'dates': dates, 'weather': weather})
        
        # analyzer
        dates, pictures, max_value_picture, max_value_name = analyzer(x_varnish)
        
        # remove entry
        db.remove(User.x_varnish == 123)
        
        self.assertEqual(max_value_picture, 'cloudy.svg')
        self.assertEqual(max_value_name, 'cloudy')
        
        #print("integration_test_analyzer: OK")


if __name__ == '__main__':
    unittest.main()