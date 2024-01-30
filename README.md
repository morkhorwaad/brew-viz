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