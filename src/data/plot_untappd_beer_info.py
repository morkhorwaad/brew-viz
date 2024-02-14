#%%
import sys
import os 
import json

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Get the root dir with config information added to path
current_dir = os.path.abspath(os.getcwd())
root_dir = os.path.join(current_dir, '..', '..')
normalized_root_path = os.path.normpath(root_dir)

if normalized_root_path not in sys.path: 
    sys.path.append(normalized_root_path)

# Load the JSON file as a python object to build DFs
from config import PROCESSED_DATA_PATH, INITIAL_DATA_PATH, MORK_COLORS

def make_horizontal_bar_chart(x, y, title, xlabel="", ylabel=""): 
    # Create bar chart
    fig, ax = plt.subplots()
    bars = ax.barh(x, y, color=MORK_COLORS["BLUE"])
    
    title_text = ax.set_title(title, loc='center', color=MORK_COLORS["BLACK"], fontweight='bold', fontsize='16', fontname="Times New Roman")
    ax.set_xlabel(xlabel, color=MORK_COLORS["BLACK"], fontsize='12', fontname="Times New Roman")
    ax.set_ylabel(ylabel, color=MORK_COLORS["BLACK"], fontsize='12', fontname="Times New Roman")
    
    # Center the title
    fig.canvas.draw()

    # Get the bounding box of the entire figure (including labels and ticks)
    renderer = fig.canvas.get_renderer()
    bbox = ax.get_tightbbox(renderer).transformed(fig.transFigure.inverted())

    # Calculate center of the plot including labels
    plot_center = (bbox.x0 + bbox.x1) / 2

    # Manually adjust the title position
    title_text.set_position([plot_center, 1.0])
    
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
                    ha='left', va='center',
                    color=MORK_COLORS["BLACK"])
        
    # Set the ticks to black and background to white
    ax.tick_params(axis='y', labelcolor=MORK_COLORS["BLACK"])
    fig.patch.set_facecolor(MORK_COLORS["WHITE"])
    ax.set_facecolor(MORK_COLORS["WHITE"])

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

    style_and_abv = beer_df.groupby(['ABV_Category', 'beer_type'])['rating_score'].mean().reset_index()
    sa_pivot = style_and_abv.pivot(index='beer_type', columns='ABV_Category', values='rating_score')
    max_rating = style_and_abv['rating_score'].max()
    min_rating = style_and_abv['rating_score'].min()
    
    # custom color map 😎 ... didn't really show the data well. my bad. 
    low_color = MORK_COLORS["LIGHTBLUE"]
    high_color = MORK_COLORS["BLUE"]
    color_map = LinearSegmentedColormap.from_list('custom_high_low', [low_color, high_color])
    
    sns.heatmap(sa_pivot, annot=True, cmap="YlGnBu", vmin=min_rating, vmax=max_rating)
    
    plt.title('Average Ratings by Beer Type and ABV', color=MORK_COLORS["BLACK"], fontweight='bold', fontsize='16', fontname="Times New Roman")
    plt.xlabel('ABV', color=MORK_COLORS["BLACK"])
    plt.ylabel('Beer Type', color=MORK_COLORS["BLACK"])
    plt.yticks(rotation=45, color=MORK_COLORS["BLACK"])
    plt.xticks(rotation=45, color=MORK_COLORS["BLACK"])
    
    plt.gcf().set_facecolor(MORK_COLORS["WHITE"])
    plt.gca().set_facecolor(MORK_COLORS["WHITE"])
    
    plt.show()
    
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

style_to_type_file = INITIAL_DATA_PATH / "beer_styles_with_types.csv"
style_df = pd.read_csv(style_to_type_file)

beer_df = pd.merge(beer_df, style_df, on='beer_style', how='left')

plot_type_vs_abv_heatmap(beer_df)
#plot_highest_rated_styles(beer_styles)
#plot_most_produced(beer_styles)
#plot_most_reviewed_styles(beer_styles)


# %%