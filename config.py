from pathlib import Path 

DATA_FOLDER_NAME = 'data'
NOTEBOOK_FOLDER_NAME = 'notebooks'

ROOT_DIR = Path(__file__).parent.absolute()
DATA_PATH = ROOT_DIR / DATA_FOLDER_NAME
NOTEBOOK_PATH = ROOT_DIR / NOTEBOOK_FOLDER_NAME
