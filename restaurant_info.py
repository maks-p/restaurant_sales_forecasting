import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime
import time

from config import yelp_api_key

class Location:

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
            'location': self.name.replace(' ', '+'),
            'limit': 10
            }

        url_params = url_params or {}
        url = '{}{}'.format(host, path)

        response = requests.get(url, headers=headers, params=url_params).json()
        
        # Set state to 'No Match' in case no Yelp match found
        state = 'No Match'
        possible_matches = []

        # Check search returns for match wtith business
        for i in range(len(response['businesses'])):

            # If match found:
            if response['businesses'][i]['name'] == self.name:

                # Local variables to help navigate JSON return
                response_ = response['businesses'][0]
                name_ = response_['name']

                print(f'Weather Location: {name_}')
                state = 'Match Found'

                #print(response['businesses'][0])
                return response_['coordinates']['latitude'], response_['coordinates']['longitude']

            else:
                
                # If no exact match, append all search returns to list
                possible_matches.append(response['businesses'][i]['name'])
        
        # If no match, show user potential matches
        if state == 'No Match':
            
            print('Exact match not found, did you mean one of the following? \n')
            
            for possible_match in possible_matches:
                print(possible_match)
                
            return None, None