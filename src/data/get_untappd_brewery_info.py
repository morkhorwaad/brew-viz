#%%
import os 
import csv
import aiohttp 
import asyncio
import json 

from aiolimiter import AsyncLimiter
from urllib.parse import urljoin

from dotenv import load_dotenv
from config import INITIAL_DATA_PATH, RETRIEVED_DATA_PATH, UNTAPPD_API_URLS

###########################
## STATIC DEFS & METHODS ##
###########################

## Setting up a request limiter: only one request every three seconds
## Untappd API only says it allows 100 requests per hour, without further specification
## This takes a while, but it works. 
limiter = AsyncLimiter(1, 3)

## Base function that takes an aiohttp.ClientSession, an API url to call, and any parameters necessary
## Returns a JSON object, or None in the case of an exception
async def fetch_json(session, url, params):
    async with limiter:
        try: 
            async with session.get(url, params=params) as response: 
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e: 
            print(f"Headers: {e.headers}")
            if 'Retry-After' in e.headers: 
                print(f"Retry-After: {e.headers['Retry-After']}")
            return None
        except aiohttp.ClientError as e: 
            print(f"Request to {url} failed: {e}")
            return None

## Wrapper for fetch_json that takes a brewery ID and creates the full request URL
async def fetch_brewery_info(session, authParams, bid): 
    print(f"Requesting info on brewery {bid}...")
    bid_url = urljoin(UNTAPPD_API_URLS["BREWERY_INFO"], bid)
    return await fetch_json(session, bid_url, authParams)
    
## Takes a dictionary of brewery_ids and untappd auth params and returns a JSON object with brewery info call results
async def get_brewery_info(brewery_info, auth_params):
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # async run a fetch for all brewery ids
        for bid in brewery_info.keys():
            task = asyncio.ensure_future(fetch_brewery_info(session, auth_params, bid))
            tasks.append(task)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # response object init
        brewery_info_response = {}
        errors = 0
        for response in responses: 
            if (response is None or                         # exception handling
                not isinstance(response, dict) or           # string response
                'meta' not in response or                   # non-API response
                not isinstance(response['meta'], dict) or   # non-API response
                response['meta'].get('code') != 200):       # API response with bad code
                
                # HANDLE ERRORS!
                errors += 1
                print("Error or bad response received!")
                
                # SHOW EM IF YOU GOTTEM
                if response is not None:
                    print(response)
            else:
                # build out brewery dictionary: key of b_id and object of all response data
                brewery_info_response[response['response']['brewery']['brewery_id']] = response['response']['brewery'] 
        
        if errors > 0:
            brewery_info_response['errors'] = errors
        
        return brewery_info_response      

##########
## MAIN ##
##########

## MAKE API PARAMS OBJECT WITH SECRETS LOADED FROM ENV FILE
load_dotenv()
UNTAPPD_CLIENT_ID = os.environ.get('untappd_client_id')
UNTAPPD_CLIENT_SECRET = os.environ.get('untappd_client_secret')

untappd_auth_params = {
    "client_id": UNTAPPD_CLIENT_ID,
    "client_secret": UNTAPPD_CLIENT_SECRET
}

## LOAD CSV FILE WITH NAMES & BREWERY_IDS
vt_bid_file = INITIAL_DATA_PATH / 'brewery_name_and_bid.csv'
vt_brewery_info = {};

with open(vt_bid_file, 'r') as file: 
    reader = csv.DictReader(file)
    for row in reader: 
        vt_brewery_info[row['bid']] = {}

## RETRIEVE BREWERY INFO & WRITE TO JSON
brewery_info_result = asyncio.run(get_brewery_info(vt_brewery_info, untappd_auth_params))
brewery_info_result_file = RETRIEVED_DATA_PATH / 'brewery_result_info.json'

with open(brewery_info_result_file, 'w') as file: 
    json.dump(brewery_info_result, file, indent=4)
    
print("FINISHED!")



# %%
