import unittest
from lab2 import *
import pandas as pd
import json



class TestSearch(unittest.TestCase):
	def test_search(self):
		api_key = read_api_key('api_key.txt')
		num_records, data = yelp_search(api_key, 'Chicago')
		names = set(list(map(lambda x: x['name'], data)))
		top3 = set(['Girl & the Goat', 'Wildberry Pancakes and Cafe', 'Au Cheval'])
		self.assertTrue(len(top3 - names) == 0, msg="Missing restaurants")



class TestAllRest(unittest.TestCase):
	def setUp(self):
		api_key = read_api_key('api_key.txt')
		self.data = all_restaurants(api_key, 'Greektown, Chicago, IL')
		self.json_resp = """
				{
			  "total": 8228,
			  "businesses": [
			    {
			      "rating": 4,
			      "price": "$",
			      "phone": "+14152520800",
			      "id": "four-barrel-coffee-san-francisco",
			      "is_closed": false,
			      "categories": [
			        {
			          "alias": "coffee",
			          "title": "Coffee & Tea"
			        }
			      ],
			      "review_count": 1738,
			      "name": "Four Barrel Coffee",
			      "url": "https://www.yelp.com/biz/four-barrel-coffee-san-francisco",
			      "coordinates": {
			        "latitude": 37.7670169511878,
			        "longitude": -122.42184275
			      },
			      "image_url": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
			      "location": {
			        "city": "San Francisco",
			        "country": "US",
			        "address2": "",
			        "address3": "",
			        "state": "CA",
			        "address1": "375 Valencia St",
			        "zip_code": "94103"
			      },
			      "distance": 1604.23,
			      "transactions": ["pickup", "delivery"]
			    }
			  ],
			  "region": {
			    "center": {
			      "latitude": 37.767413217936834,
			      "longitude": -122.42820739746094
			    }
			  }
			}
			"""

	def test_all_rest(self):
		top3 = set(['Greek Islands Restaurant', 'Meli Cafe & Juice Bar', 'Artopolis'])
		rest_names = set(map(lambda x:x['name'], self.data))
		self.assertTrue(len(top3 - rest_names) == 0, msg="Missing restaurants")

	def test_parse_api(self):
		urls = parse_api_response(self.json_resp)
		url = 'https://www.yelp.com/biz/four-barrel-coffee-san-francisco'
		self.assertTrue(url in urls, msg="Missing parsed URLs")



class TestParsePage(unittest.TestCase):
	def test_parse_first_page(self):
		response = requests.get('https://www.yelp.com/biz/the-jibarito-stop-chicago-2')
		cur_reviews, url = parse_page(response.text)
		self.assertTrue(len(cur_reviews) == 20)
		self.assertTrue(url == 'https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=20', msg="Invalid URL returned")

	def test_parse_last_page(self):
		response = requests.get('https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=210')
		cur_reviews, url = parse_page(response.text)
		self.assertTrue(url is None)


class TestExtractReviews(unittest.TestCase):
	def test_extract_reviews(self):
		reviews = extract_reviews('https://www.yelp.com/biz/the-jibarito-stop-chicago-2')
		self.assertTrue(abs(len(reviews) - 216) < 20, msg="Number of reviews should be close to 216")
		first = reviews[0]
		self.assertTrue('user_id' in first and 'rating' in first and 'date' in first and 'text' in first, msg="Incorrect review format")