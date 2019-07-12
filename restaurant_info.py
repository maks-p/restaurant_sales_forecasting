import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime
import time

from config import yelp_api_key

class restaurantLocation:

    def __init__(self, name, location):

        self.name = name
        self.location = location

    def get_lat_long(self):

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
        
        # Set state to 'No Match' in case no Yelp match found
        state = 'No Match'
        possible_matches = []

        try:
            # Check search returns for match with business
            for i in range(len(response['businesses'])):

                # If match found:
                if response['businesses'][i]['name'] == self.name:

                    # Local variables to help navigate JSON return
                    response_ = response['businesses'][0]
                    name_ = response_['name']

                    print(f'Weather Location: {name_}')
                    state = 'Match Found'

                    #return (response['businesses'][0])
                    return response_['coordinates']['latitude'], response_['coordinates']['longitude']

                else:
                    
                    # If no exact match, append all search returns to list
                    possible_matches.append(response['businesses'][i]['name'])
        except:
            pass

        # If no match, show user potential matches
        if state == 'No Match':
            
            if len(possible_matches) > 0:

                print('Exact match not found, please input one of the following venues: \n')
                for possible_match in possible_matches:
                    print(possible_match)
            
            else:
                print('No matches found, please enter a proper venue name.')
                
            return None, None
