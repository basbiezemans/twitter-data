import unittest
from requests import put, get
from datetime import date

class TestApi(unittest.TestCase):

    def test_search_bad_request(self):
        data = get('http://localhost:5000/search/')
        self.assertEqual(data.status_code, 404)

    def test_collect_bad_request(self):
        data = get('http://localhost:5000/collect/')
        self.assertEqual(data.status_code, 404)

    def test_search(self):
        today = str(date.today())
        data = get('http://localhost:5000/search/{}/37.781157,-122.398720,10mi'.format(today)).json()
        self.assertGreater(len(data.get('tweets')), 0)
    
    def test_collect(self):
        data = get('http://localhost:5000/collect/37.781157,-122.398720,10mi').json()
        self.assertGreater(len(data.get('tweets')), 0)
    
    def test_schedule(self):
        item = {
            'timestamp': '2018-07-25 12:00:00', 
            'latitude': 37.781157, 
            'longitude': -122.398720
        }
        data = put('http://localhost:5000/schedule/', data=item).json()
        self.assertEqual(data.get('timestamp'), item.get('timestamp'))
        self.assertEqual(data.get('latitude'), item.get('latitude'))
        self.assertEqual(data.get('longitude'), item.get('longitude'))