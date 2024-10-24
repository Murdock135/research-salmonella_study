import pandas as pd
import io

def get_df_info(df):
    buffer = io.StringIO()
    df.info(verbose=True, buf=buffer)
    return buffer.getvalue()


if __name__ == "__main__":
    MMG_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/MMG/MMG2022_2020-2019Data_ToShare.xlsx"
    SVI_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/social_vulnerability_index/SVI_2022_US_county.csv"
    PN_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/PulseNet data/Export_2020-2023.xlsx"
    RawPoultry_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/FSIS_raw_poultry/Dataset_RawPoultry_Current/FSIS_Raw_Poultry_Current_Extracted_2024_04_23.csv"

    MMG_df = pd.read_excel(MMG_path, sheet_name='County')
    SVI_df = pd.read_csv(SVI_path)
    PN_df = pd.read_excel(PN_path, sheet_name='2020-2023')
    RawPoultry_df = pd.read_csv(RawPoultry_path)

    dfs = {'Map the meal gap': MMG_df,
        'Social Vulnerability Index': SVI_df,
        'PulseNet': PN_df,
        'RawPoultry': RawPoultry_df}

    # Create txt file
    file_content = ""

    for name, df in dfs.items():
        file_content += f"Dataset: {name}\n"
        file_content += f"Data info:\n{get_df_info(df)}\n\n"

    # Save the file
    with open("c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/data_info.txt", "w", encoding="utf-8") as f:
        f.write(file_content)

    print(0)
