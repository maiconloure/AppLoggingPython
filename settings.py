import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get('PROJECT_ID')

TIMEOUT = os.environ.get('TIMEOUT')

DATASET_ID = os.environ.get('DATASET_ID')
TABLE_ID = os.environ.get('TABLE_ID')