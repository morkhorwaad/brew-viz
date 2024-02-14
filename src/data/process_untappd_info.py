#%%
import sys
import os 
import json

from dateutil import parser
from datetime import datetime

import pandas as pd

# we'll play around with this later...
#from structures import UntappdBeerSchema, UntappdBreweryLocationSchema, UntappdBreweryRatingSchema, UntappdBrewerySchema

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path: 
    sys.path.append(normalized_root_path)

# Load the JSON file as a python object to build DFs
from config import RETRIEVED_DATA_PATH, PROCESSED_DATA_PATH

RETRIEVED_UNTAPPD_DATA_FILE = RETRIEVED_DATA_PATH / 'brewery_result_info.json'

def sanitize_number(value):
    """
    Sanitizes an input for storage as a number. Tries to convert the input to a float or int.
    If the conversion fails, returns -1.

    Parameters:
    - value: The input value to sanitize.

    Returns:
    - A numeric value (int or float) if the input can be converted, otherwise -1.
    """
    try:
        # Try converting to a float first (to catch both ints and floats)
        num = float(value)
        # If the result is an integer, convert it to an int type
        if num.is_integer():
            return int(num)
        return num
    except ValueError:
        # Return -1 if conversion fails
        return -1
def sanitize_string(value):
    """
    Sanitizes a string for CSV storage. This function escapes double quotes,
    replaces newlines with spaces, and ensures the string is enclosed in double quotes
    if it contains commas or double quotes.

    Parameters:
    - value (str): The string to sanitize.

    Returns:
    - str: The sanitized string.
    """
    
    if value is None:
        return ""
    # Convert to string in case the value is not a string
    value = str(value)
    # Replace newline characters with spaces
    value = value.replace("\n", " ").replace("\r", " ")
    # Escape double quotes
    value = value.replace('"', '""')
    # Enclose in double quotes if the value contains commas or double quotes
    if "," in value or '"' in value:
        value = f'"{value}"'
    return value

def sanitize_date(date_str):
    """
    Converts a date string into the standardized format 'YYYY-MM-DD'.
    If the input is not a recognizable date format, an exception will be raised.
    
    Args:
    date_str (str): The date string to be sanitized.
    
    Returns:
    str: The sanitized date string in 'YYYY-MM-DD' format.
    """
    try:
        # Attempt to parse the date string using dateutil.parser
        parsed_date = parser.parse(date_str)
        
        # Format the date as YYYY-MM-DD
        sanitized_date = parsed_date.strftime('%Y-%m-%d')
        
        return sanitized_date
    except ValueError as e:
        # Raise an exception if the date_str cannot be parsed
        raise ValueError(f"Could not parse the date string '{date_str}': {e}")


def extract_untappd_info():
    # open the stored JSON file
    with open(RETRIEVED_UNTAPPD_DATA_FILE, 'r') as file:
        raw_untappd_data = json.load(file)

    # Make starting dicts of info we want to separate
    brewery_info = []
    beer_info = []
    checkin_info = []
    
    for ut_brewery_id, ut_brewery in raw_untappd_data.items(): 
        # extract the basic brewery information 
        new_brewery = {
            'brewery_id': ut_brewery_id,
            'brewery_name': sanitize_string(ut_brewery['brewery_name']),
            'brewery_in_production': sanitize_number(ut_brewery['brewery_in_production']),
            'is_independent': sanitize_number(ut_brewery['is_independent']),
            'beer_count': sanitize_number(ut_brewery['beer_count']),
            'brewery_type': sanitize_string(ut_brewery['brewery_type']),
            'rating_count': sanitize_number(ut_brewery['rating']['count']),
            'rating_score': sanitize_number(ut_brewery['rating']['rating_score']),
            'brewery_description': sanitize_string(ut_brewery['brewery_description']),
            'brewery_address': sanitize_string(ut_brewery['location']['brewery_address']),
            'brewery_city': sanitize_string(ut_brewery['location']['brewery_city']),
            'brewery_lat': sanitize_number(ut_brewery['location']['brewery_lat']),
            'brewery_lng': sanitize_number(ut_brewery['location']['brewery_lng'])
        }
        brewery_info.append(new_brewery)
    
        # get all the beer information stored away 
        for beer_item in ut_brewery['beer_list']['items']:
            beer = beer_item['beer']
            new_beer = {
                'beer_id': sanitize_number(beer['bid']),
                'brewery_id': ut_brewery_id,
                'beer_name': sanitize_string(beer['beer_name']), 
                'beer_style': sanitize_string(beer['beer_style']),
                'beer_abv': sanitize_number(beer['beer_abv']),
                'beer_ibu': sanitize_number(beer['beer_ibu']), 
                'created_at': sanitize_date(beer['created_at']), 
                'rating_score': sanitize_number(beer['rating_score']),
                'rating_count': sanitize_number(beer['rating_count']),
                'total_count': sanitize_number(beer_item['total_count'])
            }
            beer_info.append(new_beer)
            
        for checkin_item in ut_brewery['checkins']['items']:
            has_venue = checkin_item['venue'] != []
            new_checkin = {
                'checkin_id': sanitize_number(checkin_item['checkin_id']),
                'brewery_id': ut_brewery_id,
                'beer_id': sanitize_number(checkin_item['beer']['bid']),
                'checkin_created_on': checkin_item['created_at'],
                'checkin_comment': sanitize_string(checkin_item['checkin_comment']),
                'checkin_rating': sanitize_number(checkin_item['rating_score']),
                'checkin_venue_category': sanitize_string(checkin_item['venue']['primary_category']) if has_venue else '',
                'checkin_location_address': sanitize_string(checkin_item['venue']['location']['venue_address']) if has_venue else '',
                'checkin_location_city': sanitize_string(checkin_item['venue']['location']['venue_city']) if has_venue else '',
                'checkin_location_state': sanitize_string(checkin_item['venue']['location']['venue_state']) if has_venue else '',
                'checkin_location_country': sanitize_string(checkin_item['venue']['location']['venue_country']) if has_venue else '',
                'checkin_location_lat': sanitize_number(checkin_item['venue']['location']['lat']) if has_venue else '',
                'checkin_location_lng': sanitize_number(checkin_item['venue']['location']['lng']) if has_venue else '',
            }
            checkin_info.append(new_checkin)
        
    return brewery_info, beer_info, checkin_info


brewery_info, beer_info, checkin_info = extract_untappd_info()
    
brewery_df = pd.DataFrame(brewery_info)
beer_df = pd.DataFrame(beer_info)
checkin_df = pd.DataFrame(checkin_info)

brewery_na_per_column = brewery_df.isna().sum()
print(f"NaN values in Brewery DF: {brewery_na_per_column}")
## RESULTS: 3 NaN values in brewery_address. Good to know...

beer_na_per_column = beer_df.isna().sum()
print(f"NaN values in Beer DF: {beer_na_per_column}")
## RESULTS: 0 NaN values. Nice. 

checkin_na_per_column = checkin_df.isna().sum()
print(f"NaN values in Checkin DF: {checkin_na_per_column}")

brewery_df_csv = PROCESSED_DATA_PATH / "normalized_brewery_data.csv"
print(f"Writing Brewery DF to {brewery_df_csv}...")
brewery_df.to_csv(brewery_df_csv)

beer_df_csv = PROCESSED_DATA_PATH / "normalized_beer_data.csv"
print(f"Writing Beer DF to {beer_df_csv}...")
beer_df.to_csv(beer_df_csv)

checkin_df_csv = PROCESSED_DATA_PATH / "normalized_checkin_data.csv"
print(f"Writing Checkin DF to {checkin_df_csv}...")
checkin_df.to_csv(checkin_df_csv)

# %%