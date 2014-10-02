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

def get_individual_entity(endpoint):
    return Entity(get_endpoint(endpoint)[0]).__dict__

class Entity:
    def __init__(self, entity_dict):
        print(entity_dict)
        if 'properties' in entity_dict:
            self.name = entity_dict['properties']['name']
        else:
            self.name = entity_dict['name']
        self.type = entity_dict['type']

        if 'path' in entity_dict:
            self.endpoint = entity_dict['path']
        else:
            self.get_additional_info(entity_dict)

 #   def get_more(self):
 #       print('.')
 #       more = get_endpoint(self.endpoint)[0]
 #       self.get_additional_info(more)

    def get_additional_info(self, more):
        if 'relationships' in more:
            self.get_images(more)
            self.get_description(more)

    def get_images(self, more_info):
        image_base = 'http://images.crunchbase.com/' 
        image_end = more_info['relationships']['primary_image']['items'][0]['path']
        self.image = image_base + image_end

    def get_description(self, more_info):
        self.description = more_info['properties']['description']
        self.short_description = more_info['properties']['short_description']

class EntityCollection:
    """An object to deal with the state inherent with pagination.

    This is the internal object that will store entities, and arrange for
    them to be loaded lazily and so on."""
    def __init__(self, endpoint, payload):
        self.raw_entities = get_endpoint(endpoint, 1, **payload)


