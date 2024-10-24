import pandas as pd
import utils
from tqdm import tqdm
import json
import numpy as np
from typing import List

pn_path = r"C:\Users\Zayan\Documents\code\personal_repos\salmonella\Data\raw_data\PulseNet data\Export_2020-2023.xlsx"

pn_data = utils.read_data(pn_path, sheet="2020-2023")

# (1) Map AntigenForm to SerotypeWGS (forward)
forward_mapping = {}

for i, AntigenForm in enumerate(tqdm(pn_data["AntigenForm"].unique())):
    df = pn_data[pn_data["AntigenForm"] == AntigenForm]
    forward_mapping[AntigenForm] = df["Serotype_wgs"].unique().tolist()

# Save as json
save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/antgenform_serotypewgs_mapping_forward.json"
with open(save_path, "w") as file:
    json.dump(forward_mapping, file, indent=4)

# save as txt
save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/antgenform_serotypewgs_mapping_forward.txt"
with open(save_path, "w") as file:
    for key, value in forward_mapping.items():
        file.write(f"{key}: {value}\n")

# (2) Map Serotype_wgs to AntigenForm (backward)
backward_mapping = {}

for wgs in tqdm(pn_data["Serotype_wgs"].unique()):
    df = pn_data[pn_data["Serotype_wgs"] == wgs]
    backward_mapping[wgs] = df["AntigenForm"].unique().tolist()

# save as json
save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/antgenform_serotypewgs_mapping_backward.json"
with open(save_path, "w") as file:
    json.dump(backward_mapping, file, indent=4)

# save as txt
save_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/processed_data/antgenform_serotypewgs_mapping_backward.txt"
with open(save_path, "w") as file:
    for key, value in backward_mapping.items():
        file.write(f"{key}: {value}\n")

# (3) Check overlapping Serotype_wgs's.
# How I found overlaps: 
# 1. Created a matrix (like a correlation matrix) with serotype_wgs's
# 2. Wherever there's an overlap, it'll be 1.

wgs_n = pn_data["Serotype_wgs"].nunique()
wgs_names = pn_data["Serotype_wgs"].unique().tolist()
matrix_arr = np.zeros((wgs_n + 1, wgs_n + 1))
matrix_df = pd.DataFrame(matrix_arr, index=wgs_names, columns=wgs_names)

def is_overlap(wgs_1: List[str], wgs_2: List[str]) -> bool:
    for s1 in wgs_1:
        if isinstance(s1, float) and np.isnan(s1):
            continue
        for s2 in wgs_2:
            if isinstance(s2, float) and np.isnan(s2):
                continue
            if s1.lower() == s2.lower():
                return True
    return False

def get_common_ele(wgs_1, wgs_2):
    commons = []
    for s1 in wgs_1:
        if isinstance(s1, float) and np.isnan(s1):
            continue
        for s2 in wgs_2:
            if isinstance(s2, float) and np.isnan(s2):
                continue
            if s1.lower() == s2.lower():
                commons.append(s1)
    return commons   

# Iterate over the upper triangle of the matrix
for i, wgs_1 in enumerate(matrix_df.index):
    for j, wgs_2 in enumerate(matrix_df.columns):
        if j > i:  # Ensures we are only looking at the upper triangle
            if is_overlap(backward_mapping[wgs_1], backward_mapping[wgs_2]):
                matrix_df.at[wgs_1, wgs_2] = 1
                matrix_df.at[wgs_2, wgs_1] = 1  # Symmetric update

                commons = get_common_ele(backward_mapping[wgs_1], backward_mapping[wgs_2])
                print(f"Serotype_wgs's {wgs_1} and {wgs_2} overlaps on {commons}")


            
    
            
