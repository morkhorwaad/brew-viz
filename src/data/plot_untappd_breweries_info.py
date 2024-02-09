#%%
import sys
import os 
import json
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path: 
    sys.path.append(normalized_root_path)

# Load the JSON file as a python object to build DFs
from config import PROCESSED_DATA_PATH, MORK_COLORS

BEER_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_beer_data.csv'
BREWERY_DATA_PATH = PROCESSED_DATA_PATH / 'normalized_brewery_data.csv'

brewery_df = pd.read_csv(BREWERY_DATA_PATH, index_col=0)

# the scale gets weird because it's very small on y and large on x, so scale the # rating counts down
desired_max_width = 500
brewery_df['dot_size'] = brewery_df['rating_count'] / (brewery_df['rating_count'].mean() / desired_max_width)
#brewery_df = brewery_df.assign(label=lambda x: x['brewery_name'] if x['dot_size'] > 500 else "")

# we can't label every brewery, so just label the top x
desired_max_labels = 12
top_most_rated = brewery_df.sort_values('rating_count', ascending=False).iloc[:desired_max_labels]
brewery_df['label'] = np.where(
    brewery_df['brewery_id'].isin(top_most_rated['brewery_id']),
    brewery_df['brewery_name'],
    ""
)

fig, ax = plt.subplots()

ax.scatter(
    brewery_df["beer_count"],
    brewery_df["rating_score"],
    s=brewery_df["dot_size"],
    c=brewery_df.index,
    alpha=0.5
)

bc_min = brewery_df['beer_count'].min()
bc_max = brewery_df['beer_count'].max()

rs_min = brewery_df['rating_score'].min()
rs_max = brewery_df['rating_score'].max()

ax.set_ylim(rs_min, rs_max)
ax.set_xlim(bc_min, bc_max)

# set up tick labels for just the high/low of the x/y values
xtick_labels = [str(xval) if xval == bc_min or xval == bc_max else '' for xval in brewery_df['beer_count']]
# Much faster operation: 0.0008609294891357422s
# Slower version: 0.0016179084777832031s
# xtick_labels_2 = np.where(
#     (brewery_df['beer_count'] == bc_min) | (brewery_df['beer_count'] == bc_max), 
#     brewery_df['beer_count'].astype(str),
#     ""
# )
ytick_labels = [str(yval) if yval == rs_min or yval == rs_max else '' for yval in brewery_df['rating_score']]

ax.set_xticks(brewery_df['beer_count'])
ax.set_xticklabels(xtick_labels, color=MORK_COLORS["BLACK"])
ax.set_yticks(brewery_df['rating_score'])
ax.set_yticklabels(ytick_labels, color=MORK_COLORS["BLACK"])

xlim = plt.xlim()
ylim = plt.ylim()

## Set up arrow labels for the most reviewed breweries
bdf_labels = brewery_df[brewery_df['label'] != '']
for i, (idx, row) in enumerate(bdf_labels.iterrows()):
    text_x = xlim[1] + (xlim[1] - xlim[0]) * 0.05  # Example: Just outside the right xlim
    text_y = ylim[0] + (ylim[1] - ylim[0]) * (i / len(bdf_labels))  # Distribute texts evenly along the y-axis
    
    ax.annotate(
        row['label'], 
        (row['beer_count'], row['rating_score']), 
        textcoords="data", 
        xytext=(text_x, text_y), 
        ha='left',
        va='center',
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3", alpha=0.5, color=MORK_COLORS["BLACK"]),
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", alpha=0.5),
        fontsize='x-small')


ax.set_title("Breweries in Vermont", loc='center', color=MORK_COLORS["BLACK"], fontweight='bold', fontsize='16', fontname="Times New Roman")
ax.set_xlabel("Number of distinct beers", loc='center', color=MORK_COLORS["BLACK"], fontsize='12')
ax.set_ylabel("Average Untappd Rating", loc='center', color=MORK_COLORS["BLACK"], fontsize='12')

fig.patch.set_facecolor(MORK_COLORS["WHITE"])
ax.set_facecolor(MORK_COLORS["WHITE"])

ax.text(0, ylim[0] - .25, 'The size of the dot represents the total number of reviews the brewery has gotten on Untappd', color=MORK_COLORS["BLACK"])

# Remove frame (spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.show()

#BUBBLE CHART


# %%