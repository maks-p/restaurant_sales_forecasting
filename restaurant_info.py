import requests
import json

from config import yelp_api_key

class Location:

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def make_api_call(self):
        host = 'https://api.yelp.com'
        path = '/v3/businesses/search'
        
        # Yelp Authorization Header with API Key
        headers = {
            'Authorization': 'Bearer {}'.format(yelp_api_key) 
        }

        url_params = {
            'term': self.name.replace(' ', '+'),
            'location': self.location.replace(' ', '+'),
            'limit': 10
            }

        url_params = url_params or {}
        url = '{}{}'.format(host, path)
        response = requests.get(url, headers=headers, params=url_params).json()

        return response

    def validate_business(self):
        response = self.make_api_call()
        
        # Set state to False in case no Yelp match found
        state = False
        possible_matches = []

        try:
            # Check search returns for match with business
            for i in range(len(response['businesses'])):

                # If match found:
                if response['businesses'][i]['name'] == self.name:
                    return response['businesses'][0]
                    state = True
        except:
            print('Venue not found, please enter a valid venue')

    def lat_long(self):
        r = self.validate_business()

        #return (response['businesses'][0])
        lat, long = r['coordinates']['latitude'], r['coordinates']['longitude']

        return lat, long

        





