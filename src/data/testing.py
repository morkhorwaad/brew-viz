#%%
import pandas as pd
import os 
from dotenv import load_dotenv
from config import DATA_PATH

load_dotenv()
UNTAPPD_CLIENT_ID = os.environ.get('untappd_client_id')
UNTAPPD_CLIENT_SECRET = os.environ.get('untappd_client_secret')

print(UNTAPPD_CLIENT_ID)
print(UNTAPPD_CLIENT_SECRET)

### READING VT BREWERY INFO FROM OPENBREWERYDB
example_brewery_list = [
    {
        "id": "6c53984f-fac1-4ea7-9c44-44e25897c71a",
        "name": "14th Star Brewing",
        "brewery_type": "micro",
        "address_1": "133 N Main St Ste 7",
        "address_2": None,
        "address_3": None,
        "city": "Saint Albans",
        "state_province": "Vermont",
        "postal_code": "05478-1735",
        "country": "United States",
        "longitude": None,
        "latitude": None,
        "phone": "8025285988",
        "website_url": "http://www.14thstarbrewing.com",
        "state": "Vermont",
        "street": "133 N Main St Ste 7"
    }
]

vt_breweries_obdb_file = DATA_PATH / 'vt_breweries_obdb.json'
brewery_df = pd.read_json(vt_breweries_obdb_file)
print(brewery_df)

brewery_names = brewery_df['name']
brewery_names_file = DATA_PATH / 'brewery_names.csv'
brewery_names.to_csv(brewery_names_file, index=False)


# %%
