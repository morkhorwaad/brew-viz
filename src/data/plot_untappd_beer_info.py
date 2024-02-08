#%%
import sys
import os 
import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_most_produced(beer_df, top_x=10, ):
    top_10_produced = beer_df.sort_values('Num_Beers', ascending=False).iloc[:10]
    fig_mpb, ax_mpb = make_horizontal_bar_chart(
        top_10_produced.index,
        top_10_produced['Num_Beers'],
        "Top 10 Most Produced Beer Styles in Vermont",
    )
    plt.show()

def plot_highest_rated_styles(beer_df, top_x=10):
    top_10_by_rating = beer_df.sort_values('Weighted_Rating', ascending=False).iloc[:10]
    top_10_by_rating['Weighted_Rating'] = top_10_by_rating['Weighted_Rating'].round(2)
    fig_br, ax_br = make_horizontal_bar_chart(
        top_10_by_rating.index,
        top_10_by_rating['Weighted_Rating'],
        "Top 10 Beer Styles in Vermont by Weighted Average Untappd Rating"
    )
    x_min = beer_df['Weighted_Rating'].mean()
    x_max = beer_df['Weighted_Rating'].max()
    
    print(x_min, x_max)
    ax_br.set_xlim(x_min, x_max)
    plt.show()

def plot_most_reviewed_styles(beer_df, top_x=10):
    top_10_by_count = beer_styles.sort_values('Total_Num_Ratings', ascending=False).iloc[:10]
    fig_bc, ax_bc = make_horizontal_bar_chart(
        top_10_by_count.index,
        top_10_by_count['Total_Num_Ratings'],
        "Top 10 Most Reviewed Beer Styles in Vermont"
    )
    plt.show()

def plot_type_vs_abv_heatmap(beer_df):
    ## FAILED CHART
    ## This chart had way too many data points on it, so i needed to group the data
    # beer_style_and_abv = beer_df.groupby(['beer_style', 'beer_abv'])['rating_score'].mean().reset_index()
    # style_and_abv_pivot = beer_style_and_abv.pivot(index='beer_style', columns='beer_abv', values='rating_score')
    # sns.heatmap(style_and_abv_pivot, annot=True, cmap="YlGnBu", vmin=-1, vmax=1)

    style_and_abv = beer_df.groupby(['ABV_Category', 'Beer_Type'])['rating_score'].mean().reset_index()
    sa_pivot = style_and_abv.pivot(index='Beer_Type', columns='ABV_Category', values='rating_score')
    max_rating = style_and_abv['rating_score'].max()
    min_rating = style_and_abv['rating_score'].min()
    
    sns.heatmap(sa_pivot, annot=True, cmap="YlGnBu", vmin=min_rating, vmax=max_rating)
    
    plt.title('Average Ratings by Beer Type and ABV')
    plt.xlabel('ABV')
    plt.ylabel('Beer Type')
    plt.xticks(rotation=45)
    
    plt.show()
    
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

# calculating a weighted rating
C = beer_styles['Avg_Rating'].mean()
m = beer_styles['Total_Num_Ratings'].quantile(0.50)

beer_styles['Weighted_Rating'] = (\
    (beer_styles['Total_Num_Ratings'] / (beer_styles['Total_Num_Ratings'] + m)) \
    * beer_styles['Avg_Rating']) \
    + ((m / (beer_styles['Total_Num_Ratings'] + m)) * C)
  
abv_bins = [0, 5, 8, 10, float('inf')]
abv_labels = ['Low (<5%)', 'Medium (5-8%)', 'High (8-10%)', 'Very High (>10%)']
beer_df['ABV_Category'] = pd.cut(beer_df['beer_abv'], bins=abv_bins, labels=abv_labels, right=False)

style_to_type = {
    'IPA': 'IPA', 
    'Stout': 'Dark', 
    'Sour': 'Sour', 
    'Märzen': 'Amber', 
    'Pale Ale': 'IPA', 
    'Scotch Ale': 'Dark', 
    'Kölsch': 'Light', 
    'Lager': 'Light', 
    'Wheat': 'Light', 
    'Pilsner': 'Light', 
    'Cream Ale': 'Light', 
    'Fruit': 'Light', 
    'Strong Ale': 'Dark',
    'Festbier': 'Light', 
    'Brown Ale': 'Dark', 
    'Red Ale': 'Amber', 
    'Farmhouse Ale': 'Sour', 
    'Wild Ale': 'Sour', 
    'Spiced': 'Amber', 
    'Kellerbier': 'Light',
    'Bitter': 'Amber', 
    'Schwarzbier': 'Amber', 
}

def map_style_to_type(beer_style):
    for key in style_to_type.keys(): 
        if(beer_style.startswith(key)): 
            return style_to_type[key]
    return 'Other'

beer_df['Beer_Type'] = beer_df['beer_style'].apply(lambda x: map_style_to_type(x))

plot_type_vs_abv_heatmap(beer_df)
#plot_highest_rated_styles(beer_styles)
#plot_most_produced(beer_styles)
#plot_most_reviewed_styles(beer_styles)


# %%