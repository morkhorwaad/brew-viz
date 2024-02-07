# VISUALIZING VERMONT BREWERY DATA!

This is a little project to put together some skills I'm learning: 
    - Python
    - pandas, numpy, matplotlib
    - requests

Right now, it's just a scaffold, but the idea is this: 

    1. Retrieve information on VT breweries from Untappd: 
        a. Make a list of all breweries in VT (semi-manually, no location filter in Untappd API)
        b. Retrieve brewery_id for all breweries in list
        c. Use brewery_id to get detailed information for all breweries (can be fully scripted)
    2. Clean the data and write out for local access
    3. Visualize! 
        a. We'll burn this bridge when we get to it. 

### SECRET REQUIREMENTS

This is using the Untappd API, so you need a root-level .env file with UNTAPPD_CLIENT_ID and UNTAPPD_CLIENT_SECRET defined in it. 


### Ideas for plotting: 
    Map of Breweries: Plot the locations of breweries on a map, using latitude and longitude if available. You can differentiate the type of breweries (micro, macro, brewpub, etc.) using different colors or symbols. This visualization can help to identify geographic concentrations of breweries and explore regional beer culture.

    Bubble Chart of Breweries by Beer Count and Ratings: Create a bubble chart where each bubble represents a brewery, plotted by the number of beers they produce (x-axis) and their average rating (y-axis). The size of the bubble can represent the total number of ratings (a proxy for popularity). This visualization can help identify standout breweries that offer both a wide selection and high-quality beers.

    Bar Chart of Beer Styles: Use a bar chart to show the number of beers by style (IPA, Stout, Lager, etc.). This can help to identify the most popular or dominant beer styles within your dataset.

    Histogram of ABV (Alcohol By Volume): A histogram can show the distribution of ABV levels across all beers. This could help to identify common ABV ranges for craft beers and how they vary across different beer styles.

    Scatter Plot of Beers by ABV and IBU: Plotting beers on a scatter plot with ABV on one axis and IBU (International Bitterness Units) on the other can reveal patterns between the strength and bitterness of beers. This visualization can help beer enthusiasts find beers that match their taste preferences.

    Heatmap of Ratings by Style and ABV: Create a heatmap to show how average ratings vary across different beer styles and ABV levels. This could help identify if certain styles or strength levels tend to be rated higher than others.

    Box Plot of Ratings by Brewery Type: Use box plots to compare the distribution of beer ratings across different types of breweries. This can reveal if certain types of breweries (like microbreweries or brewpubs) tend to have higher-rated beers.

    Correlation Matrix: Create a correlation matrix of numerical variables (number of beers, number of ratings, average rating, ABV, IBU) to explore potential relationships between them. This can help identify if factors like ABV are related to higher ratings or if breweries with more beers get more ratings.