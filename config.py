from pathlib import Path 
from urllib.parse import urljoin

## PATH VARIABLES
DATA_FOLDER_NAME = 'data'
NOTEBOOK_FOLDER_NAME = 'notebooks'

ROOT_DIR = Path(__file__).parent.absolute()

DATA_PATH = ROOT_DIR / DATA_FOLDER_NAME
INITIAL_DATA_PATH = DATA_PATH / "initial"
RETRIEVED_DATA_PATH = DATA_PATH / "retrieved"
PROCESSED_DATA_PATH = DATA_PATH / "processed"

NOTEBOOK_PATH = ROOT_DIR / NOTEBOOK_FOLDER_NAME

## API VARIABLES
UNTAPPD_API_BASE_URL = 'https://api.untappd.com/v4/'
UNTAPPD_API_URLS = {
    "BREWERY_SEARCH": urljoin(UNTAPPD_API_BASE_URL, "search/brewery/"),
    "BREWERY_INFO": urljoin(UNTAPPD_API_BASE_URL, "brewery/info/"),
    "BEER_SEARCH": urljoin(UNTAPPD_API_BASE_URL, "search/beer/"),
    "BEER_INFO": urljoin(UNTAPPD_API_BASE_URL, "beer/info/"),
}

MORK_COLORS = {
    "BLACK": "#414141",
    "WHITE": "#e7e5d6",
    "BLUE": "#266DD3",
    "LIGHTBLUE": "#93c5e2"
}
