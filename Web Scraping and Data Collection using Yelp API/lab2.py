import io, time, json
import requests
from bs4 import BeautifulSoup

def read_api_key(filepath):
    """
    Read the Yelp API Key from file.
    
    Args:
        filepath (string): File containing API Key
    Returns:
        api_key (string): The API Key
    """
    
    # feel free to modify this function if you are storing the API Key differently
    with open(filepath, 'r') as f:
        return f.read().replace('\n','')




def yelp_search(api_key, query, offset=0):
    """
    Make an authenticated request to the Yelp API.

    Args:
        query (string): Search term

    Returns:
        total (integer): total number of businesses on Yelp corresponding to the query
        businesses (list): list of dicts representing each business
    """
    
    #[YOUR CODE HERE]
    url = 'https://api.yelp.com/v3/businesses/search'
    url_params = {'location':query.replace(' ','+').replace(' ',''), 'offset':offset}
    header = {'Authorization': 'Bearer %s' % api_key}
    
    response = requests.get(url, headers = header, params=url_params)
    resp_dict = response.json()
    
    return resp_dict['total'], resp_dict['businesses']
    
    
    



def all_restaurants(api_key, query):
    """
    Retrieve ALL the restaurants on Yelp for a given query.

    Args:
        query (string): Search term

    Returns:
        results (list): list of dicts representing each restaurant
    """
    offset = 0  
    num_records, data = yelp_search(api_key, 'Chicago')
    url = 'https://api.yelp.com/v3/businesses/search'
    url_params = {'categories': 'restaurants, All','location':query.replace(' ','+').replace(' ',''), 'offset':offset, 'limit':50}
    header = {'Authorization': 'Bearer %s' % api_key}
    response_list = []
    response = requests.get(url, headers = header, params=url_params)
    resp_dict = response.json()
    total_keys = resp_dict['total']
    
    n_call = total_keys/50
    
    while n_call > 0:
        response = requests.get(url, headers = header, params=url_params)
        time.sleep(0.2)
        resp_dict = response.json()
        for res in resp_dict['businesses']:
            response_list.append(res)
        offset = offset + 50
        n_call = n_call - 1 
        url_params = {'categories': 'restaurants, All','location':query.replace(' ','+').replace(' ',''), 'offset':offset, 'limit':50}
        #print (url_params)
        
    return response_list
    


def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    #[YOUR CODE HERE]
    url_list =[]
    dict_data = json.loads(data)
    for business in dict_data['businesses']:
        url_list.append(business['url'])
    return url_list

    
    



def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.prettify())
    url_next = soup.find('link',rel='next')
    if url_next:
        url_next = url_next.get('href')
    else:
        url_next = None

    reviews = soup.find_all('div', itemprop="review")
    
    reviews_list = []
    for r in reviews:
        
        #[YOUR CODE HERE]
        author = r.find("meta",  itemprop="author")["content"]
        rating = r.find("meta", itemprop="ratingValue")["content"]
        date = r.find("meta", itemprop="datePublished")["content"]
        text = r.p.text
        reviews_list.append({'user_id': str(author), 'rating': float(rating), 'date': str (date), 'text': str(text)}) 
        
    #print(reviews_list)
    return reviews_list, url_next




def extract_reviews(url):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """

    #[YOUR CODE HERE]
    reviews = []
    resp = requests.get(url)
    rev,url_next = parse_page(resp.text)
    for review in rev:
        reviews.append(review)
    while url_next is not None:
        resp = requests.get(url_next)
        rev,url_next = parse_page(resp.text)
        for review in rev:
            reviews.append(review)
    return reviews




