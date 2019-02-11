import json
from lab2 import *
import requests


api_key = read_api_key('api_key.txt')

num_records, data = yelp_search(api_key, 'Chicago')
with open('search.json', 'w') as fout:
	fout.write(json.dumps(data))

data = all_restaurants(api_key, 'Greektown, Chicago, IL')
with open('all_rest.json', 'w') as fout:
	fout.write(json.dumps(data))

response = requests.get('https://www.yelp.com/biz/the-jibarito-stop-chicago-2')
cur_reviews, url = parse_page(response.text)
with open('fp_reviews.json', 'w') as fout:
	fout.write(json.dumps(cur_reviews))



response = requests.get('https://www.yelp.com/biz/the-jibarito-stop-chicago-2?start=210')
cur_reviews, url = parse_page(response.text)
with open('lp_reviews.json', 'w') as fout:
	fout.write(json.dumps(cur_reviews))


reviews = extract_reviews('https://www.yelp.com/biz/the-jibarito-stop-chicago-2')
with open('reviews.json', 'w') as fout:
	fout.write(json.dumps(reviews))