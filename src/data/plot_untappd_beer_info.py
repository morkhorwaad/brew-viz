#%%
import sys
import os 
import json

import pandas as pd
import matplotlib.pyplot as plt

def make_horizontal_bar_chart(x, y, title, xlabel="", ylabel=""): 
    # Create bar chart
    fig, ax = plt.subplots()
    bars = ax.barh(x, y, color='skyblue')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Remove frame (spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Remove x-axis tick marks and labels
    ax.xaxis.set_ticks_position('none') 
    ax.set_xticklabels([])

    # Add value labels to the right of each bar
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width}',
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center')

    # Hide y-axis tick marks
    plt.tick_params(axis='y', which='both', length=0)
    
    return fig, ax

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path: 
    sys.path.append(normalized_root_path)

# Load the JSON file as a python object to build DFs
from config import PROCESSED_DATA_PATH

BEER_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_beer_data.csv'
BREWERY_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_brewery_data.csv'

beer_df = pd.read_csv(BEER_DATA_PATH, index_col=0)

beer_styles = beer_df.groupby('beer_style').agg(
    Num_Beers=('beer_style', 'count'),
    Avg_Abv=('beer_abv', 'mean'),
    Avg_Ibu=('beer_ibu', 'mean'),
    Avg_Rating=('rating_score', 'mean'),
    Total_Num_Ratings=('rating_count', 'sum')
)

top_10_produced = beer_styles.sort_values('Num_Beers', ascending=False).iloc[:10]
fig_mpb, ax_mpb = make_horizontal_bar_chart(
    top_10_produced.index,
    top_10_produced['Num_Beers'],
    "Top 10 Most Produced Beer Styles in Vermont",
)

top_10_by_rating = beer_styles.sort_values('Avg_Rating', ascending=False).iloc[:10]
top_10_by_rating['Avg_Rating'] = top_10_by_rating['Avg_Rating'].round(2)
fig_br, ax_br = make_horizontal_bar_chart(
    top_10_by_rating.index,
    top_10_by_rating['Avg_Rating'],
    "Top 10 Beer Styles in Vermont by Average Untappd Rating"
)

top_10_by_count = beer_styles.sort_values('Total_Num_Ratings', ascending=False).iloc[:10]
fig_bc, ax_bc = make_horizontal_bar_chart(
    top_10_by_count.index,
    top_10_by_count['Total_Num_Ratings'],
    "Top 10 Most Reviewed Beer Styles in Vermont"
)

plt.show()


# %%