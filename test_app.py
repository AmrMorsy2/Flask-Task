import unittest
import requests
import random
from modules import rowItem

class TestApp(unittest.TestCase):

    def test_search(self):
        ret = requests.get('http://localhost:5000/search?name=luke')
        self.assertEqual(ret.status_code, 200)

    def test_ListItem(self):
        for i in range(5):
            res = requests.get('https://swapi.dev/api/people/'+str(random.randint(1, 80))).json()
            ret = rowItem.ListItem(res)
            self.assertNotEqual(ret.name, None)
            self.assertNotEqual(ret.gender, None)
            self.assertNotEqual(ret.speciesName, None)
            self.assertNotEqual(ret.averagelifeSpan, None)
            self.assertNotEqual(ret.homePlanet, None)
            self.assertNotEqual(ret.movieList, [])

if __name__ == '__main__':
    unittest.main()