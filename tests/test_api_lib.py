import unittest
from app.api_lib import filter_items

class TestApiLib(unittest.TestCase):

    def test_filter_items(self):
        r = [{
            'created_at': 'Fri Jul 20 01:28:11 +0000 2018',
            'foo': 1,
            'id': 1020118136605962240,
            'bar': 'baz', 
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        }]
        item = filter_items(r)[0]
        self.assertEqual(list(item), ['created_at', 'id', 'text'])