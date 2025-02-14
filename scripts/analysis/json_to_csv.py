import json
import pandas as pd
import os
from typing import Dict
import argparse


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


def main():
    parser = argparse.ArgumentParser(description='Convert JSON file to CSV format')
    parser.add_argument('input_json', help='Path to the input JSON file')
    parser.add_argument('output_dir', help='Name of the output directory (will be created in data/processed/)')
    args = parser.parse_args()

    # Use the provided JSON file path
    with open(args.input_json, "r") as file:
        raw_dict = json.load(file)

    # Create output directory using the user-provided name
    data_save_path = os.path.join('data', 'processed', args.output_dir)
    os.makedirs(data_save_path, exist_ok=True)
    
    raw_dict = raw_dict[0]
    metadata = raw_dict["metadata"]
    data = raw_dict["data"]
    appendix = raw_dict["appendix"]
    
    metadata_to_csvs(data, data_save_path)
    print(f"CSV files have been created successfully in {data_save_path}/")

if __name__ == "__main__":
    main()
