import json
import requests
import os
import sys

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
        results.append(get_endpoint_page(endpoint, i, payload))
    return results

def get_endpoint_page(endpoint, page, payload):
    payload = new_payload(page=str(page), **payload)
    r = requests.get(base_url + endpoint, params=payload)
    return r.json()['data']['items']

if __name__ == "__main__":
    companies = get_endpoint('organizations', 1, organization_types="company")
    print(companies)
