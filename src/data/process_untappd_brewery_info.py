#%%
import sys
import os 
import json

import pandas as pd

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path: 
    sys.path.append(normalized_root_path)

# Load the JSON file as a python object to build DFs
from config import RETRIEVED_DATA_PATH, PROCESSED_DATA_PATH

raw_untappd_data_file = RETRIEVED_DATA_PATH / 'brewery_result_info.json'
with open(raw_untappd_data_file, 'r') as file:
    raw_untappd_data = json.load(file)

# Make starting dicts of info we want to separate
brewery_info = {}
beer_info = []

## TODO: extract these into separate functions that include sanitization / checking
for brewery_id, brewery in raw_untappd_data.items(): 
    
    # extract the basic brewery information 
    brewery_info[brewery_id] = {
        'brewery_name': brewery['brewery_name'],
        'brewery_in_production': brewery['brewery_in_production'],
        'is_independent': brewery['is_independent'],
        'beer_count': brewery['beer_count'],
        'brewery_type': brewery['brewery_type'],
        'rating_count': brewery['rating']['count'],
        'rating_score': brewery['rating']['rating_score'],
        'brewery_description': brewery['brewery_description'],
        'brewery_address': brewery['location']['brewery_address'],
        'brewery_city': brewery['location']['brewery_city'],
        'brewery_lat': brewery['location']['brewery_lat'],
        'brewery_lng': brewery['location']['brewery_lng']
    }
    
    # get all the beer information stored away 
    for beer_item in brewery['beer_list']['items']:
        beer = beer_item['beer']
        new_beer = {
            'brewery_id': brewery_id,
            'beer_id': beer['bid'],
            'beer_name': beer['beer_name'], 
            'beer_style': beer['beer_style'],
            'beer_abv': beer['beer_abv'],
            'beer_ibu': beer['beer_ibu'], 
            'created_at': beer['created_at'], 
            'rating_score': beer['rating_score'],
            'rating_count': beer['rating_count'],
            'total_count': beer_item['total_count']
        }
        beer_info.append(new_beer)
    
brewery_df = pd.DataFrame.from_dict(brewery_info, orient='index')
beer_df = pd.DataFrame(beer_info)

# print(brewery_df.head())
# print(beer_df.head())

brewery_na_per_column = brewery_df.isna().sum()
print(f"NaN values in Brewery DF: {brewery_na_per_column}")
## RESULTS: 3 NaN values in brewery_address. Good to know...

beer_na_per_column = beer_df.isna().sum()
print(f"NaN values in Beer DF: {beer_na_per_column}")
## RESULTS: 0 NaN values. Nice. 

brewery_df_csv = PROCESSED_DATA_PATH / "normalized_brewery_data.csv"
print(f"Writing Brewery DF to {brewery_df_csv}...")
brewery_df.to_csv(brewery_df_csv)

beer_df_csv = PROCESSED_DATA_PATH / "normalized_beer_data.csv"
print(f"Writing Beer DF to {beer_df_csv}...")
beer_df.to_csv(beer_df_csv)

# %%