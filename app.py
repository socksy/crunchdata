import json
import requests
import os
import sys

base_url = "http://api.crunchbase.com/v/2/"
try:
    key = os.environ["CRUNCHKEY"]
except KeyError:
    print("Please export CRUNCHKEY as your crunchbase api_key (have you"    
            + " sourced ./secrets.sh ?)")
    sys.exit(1)

payload = { "user_key": key}
r = requests.get(base_url +'organizations', params=payload)
print(r.text)
