import requests
import sys
import os

base_url = "http://api.crunchbase.com/v/2/"
try:
    user_key = os.environ["CRUNCHKEY"]
except KeyError:
    print("Please export CRUNCHKEY as your crunchbase api_key (have you"    
            + " sourced ./secrets.sh ?)")
    sys.exit(1)

def new_payload(**contents):
    base_payload = { "user_key": user_key}
    base_payload.update(contents)
    return base_payload

def get_endpoint(endpoint, pages=1, **payload):
    results = []
    for i in range(pages):
        results.extend(get_endpoint_page(endpoint, i, payload))
    return results

def get_endpoint_page(endpoint, page, payload):
    payload = new_payload(page=str(page), **payload)
    r = requests.get(base_url + endpoint, params=payload)

    results = r.json()['data']
    if 'error' in results:
        return []
    elif 'items' in results:
        return results['items']
    else:
        return [results]

class Entity:
    def __init__(self, entity_dict):
        self.name = entity_dict['name']
        self.type = entity_dict['type']
        sys.stdout.write('-')
        if 'path' in entity_dict:
            self.endpoint = entity_dict['path']

    def get_additional_info(self):
        print('.')
        more = get_endpoint(self.endpoint)[0]
        self.get_images(more)

    def get_images(self, more_info):
        image_base = 'http://images.crunchbase.com/' 
        image_end = more_info['relationships']['primary_image']['items'][0]['path']
        self.image = image_base + image_end
