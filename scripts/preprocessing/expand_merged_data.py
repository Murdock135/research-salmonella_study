import pandas as pd
import os
from thefuzz import process, fuzz
from salmonella_study import utils
from salmonella_study import data_processing as processing
from salmonella_study.config import Config
from merge_datasets import merge

if __name__ == "__main__":
    # create list of states
    
    processed_data_path = Config.PROCESSED_DATA_DIR
    raw_data_path = Config.RAW_DATA_DIR
    year = 2020

    svi_data = pd.read_csv(os.path.join(raw_data_path, 'social_vulnerability_index', f''))