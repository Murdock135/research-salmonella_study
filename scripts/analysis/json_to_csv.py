import json
import pandas as pd
from typing import Dict

file_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/usda_fsis_lab_sampling_dataset_public_sample.json"
save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/fsis"

with open(file_path, "r") as file:
    raw_dict = json.load(file)


def metadata_to_csvs(metadata_dict: Dict, save_path, prefix='metadata'):
    metadata_list = []

    for key, val in metadata_dict.items():

        if isinstance(val, dict):
            metadata_list.append([key, f"See csv named {key}.csv"])
            metadata_to_csvs(val, save_path, key)
        elif isinstance(val, list):
            metadata_list.append([key, f"See csv named {key}.csv"])
            df = pd.DataFrame(val)
            df.to_csv(f"{save_path}/{key}.csv", index=False)
        else:
            metadata_list.append([key, val])

    metadata_df = pd.DataFrame(metadata_list)
    metadata_df.to_csv(f"{save_path}/{prefix}.csv", index=False)



raw_dict = raw_dict[0]
metadata = raw_dict["metadata"]
data = raw_dict["data"]
appendix = raw_dict["appendix"]

data_save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/fsis/data"
metadata_to_csvs(data, data_save_path)
print("Excel file has been created successfully.")
