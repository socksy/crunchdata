import json
import requests
import os
import sys
from flask import Flask, render_template
app = Flask(__name__)

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
       print('.')
       if 'path' in entity_dict:
           self.endpoint = entity_dict['path']
           more = get_endpoint(self.endpoint)[0]

           image_end = more['relationships']['images']['items'][0]['path']
           image_base = 'http://images.crunchbase.com/' 
           self.image = image_base + image_end
    
def get_companies():
    raw_companies = get_endpoint('organizations', 1, organization_types="company")
    #TODO change this so we can sanely deal with pagination
    raw_companies = raw_companies[:10] 
    companies = []
    for company in raw_companies:
        companies.append(Entity(company))
    return companies

#ugly hack to get something in global scope for the time being
companies = None
@app.route('/')
def companies():

    return render_template('companies.html', companies=companies)

if __name__ == "__main__":
#    companies = get_endpoint('organizations', 1, organization_types="company")
#    print(companies)
    companies = get_companies()
    print (companies)
    app.run()
