# %%
import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path:
    sys.path.append(normalized_root_path)

from config import PROCESSED_DATA_PATH, INITIAL_DATA_PATH, MORK_COLORS

# CSV File locations
BEER_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_beer_data.csv'
BREWERY_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_brewery_data.csv'
CHECKIN_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_checkin_data.csv'

### MAIN ###

# Load dataframes
brewery_df = pd.read_csv(BREWERY_DATA_PATH, index_col=0)
beer_df = pd.read_csv(BEER_DATA_PATH, index_col=0)
checkin_df = pd.read_csv(CHECKIN_DATA_PATH, index_col=0)

# merge styles to types to get a more consolidated 'type' of beer
style_to_type_file = INITIAL_DATA_PATH / "beer_styles_with_types.csv"
style_df = pd.read_csv(style_to_type_file)

beer_df = pd.merge(
    beer_df, 
    style_df, 
    on='beer_style', 
    how='left')

checkin_with_style = pd.merge(
    checkin_df, 
    beer_df, 
    on='beer_id', 
    how='left', 
    suffixes=['_chk', '_beer'])

checkin_with_style = checkin_with_style[['checkin_id', 'checkin_created_on', 'beer_type']]
checkin_with_style['checkin_created_on'] = pd.to_datetime(checkin_with_style['checkin_created_on'])

checkin_by_date_and_style = checkin_with_style.groupby(['beer_type', pd.Grouper(key='checkin_created_on', freq='D')]).count().reset_index()
pivot_df = checkin_by_date_and_style.pivot(index='checkin_created_on', columns='beer_type', values='checkin_id')
pivot_df = pivot_df.fillna(method='ffill')

cumulative_df = pivot_df.cumsum()

year_slice = cumulative_df.loc["2024":]
smoothed = year_slice.rolling(window=7).mean()

smoothed.plot(kind='line')

plt.figure(figsize=(12, 6))
plt.show()

#checkin_by_date_and_style.plot(x='checkin_created_on', y='checkin_id')
#plt.show()

# %%