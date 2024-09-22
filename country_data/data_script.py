#!/usr/bin/python3
""" Get state, LGA datas"""

import requests
import json

def get_state():
    """ Get state/ADM1 data of a country"""

    admin_level = 'ADM1'
    url = "http://api.geonames.org/searchJSON?q=Nigeria&fuzzy=1.0&username=akinniyi&maxRows=1000&featureCode=ADM1&featureClass=A"

    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()

    else:
        error = {
            'status_code': r.status_code,
            'message': r.content
        }
        print(error)

    # Save the data to a file
    with open('state.json', 'w') as f:
        json.dump(result, f, indent=4)

def get_LGA():
    """ Get LGA/ADM2 data of a country"""

    admin_level = 'ADM2'
    url = "http://api.geonames.org/searchJSON?q=Nigeria&fuzzy=1.0&username=akinniyi&maxRows=1000&featureCode=ADM2&featureClass=A"

    r = requests.get(url)
    if r.status_code == 200:
        result = r.json()

    else:
        error = {
            'status_code': r.status_code,
            'message': r.content
        }
        print(error)

    # Save the data to a file
    with open('LGA.json', 'w') as f:
        json.dump(result, f, indent=4)

get_state()
get_LGA()