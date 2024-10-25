import pandas as pd
from thefuzz import process
from salmonella_study import utils
import sys
from tqdm import tqdm

# Function to extract population data
def get_population(population_xlsx_path, state_long=None, year=None) -> pd.DataFrame:
    population_xlsx = pd.ExcelFile(population_xlsx_path)
    sheet_name = population_xlsx.sheet_names[0]  # census population xlsx file has only 1 sheet
    population_data = pd.read_excel(population_xlsx, sheet_name=sheet_name, skiprows=3)  # first 3 rows are irrelevant
    population_data = population_data[:-6]  # last 6 rows are irrelevant
    population_data = population_data.drop(columns=population_data.columns[1])  # 2nd column is irrelevant
    population_data.rename(columns={population_data.columns[0]: "County"}, inplace=True)

    if state_long is not None:
        population_data = population_data.loc[population_data['County'].str.lower().str.contains(state_long.lower())].reset_index(drop=True)
    else:
        population_data = population_data.iloc[1:, :]  # Remove row corresponding to 'United States of America'
        population_data["County"] = population_data["County"].str.lstrip('.')
        population_data["County"] = population_data["County"].str.strip()
        population_data["County"] = population_data["County"].str.title()
        population_data["State"] = population_data['County'].apply(lambda x: x.split(',')[-1].strip())

        # Put state column after county column
        state_col = population_data.pop('State')
        population_data.insert(1, 'State', state_col)

        if year is not None:
            if str(year) in population_data.columns:
                return population_data[["County", "State", str(year)]]
            else:
                print(f"Year {year} not found in population data.")
                sys.exit(1)
        return population_data

# Function to match counties using fuzzy matching
def match_counties(county, list_of_counties, cutoff=90):
    """Match a county with similar counties from another list using fuzz"""
    match = process.extractOne(county, list_of_counties, score_cutoff=cutoff)
    if match:
        return match[0]
    return None

def pad_list(list_to_pad, target_length):
    """Pad the list with None until it reaches the target length"""
    return list_to_pad + [None] * (target_length - len(list_to_pad))

def append_state_name(county_name, state_name):
    if county_name is not None:
        return f"{county_name}, {state_name}".title()
    else:
        print(f"County name is None for {state_name}")
        return None

# Main function to load data and match counties
if __name__ == "__main__":
    processed_data_path = (r"C:\Users\Zayan\Documents\code\personal_repos\salmonella\Data\processed_data")
    results_path = r"C:\Users\Zayan\Documents\code\personal_repos\salmonella\results"

    # Specify year and state
    year = 2020
    state = 'MO'
    state_long = 'Missouri'

    # File paths for the datasets
    svi_path = f"C:\\Users\\Zayan\\Documents\\code\\personal_repos\\salmonella\\Data\\raw_data\\social_vulnerability_index\\SVI_{year}_US_county.csv"
    pn_path = r"C:\Users\Zayan\Documents\code\personal_repos\salmonella\Data\raw_data\PulseNet data\Export_2020-2023.xlsx"
    mmg_path = r"c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/MMG/MMG2022_2020-2019Data_ToShare.xlsx"
    pop_data_path = "c:/Users/Zayan/Documents/code/personal_repos/salmonella/Data/raw_data/census data/usa_2020_to_2023.xlsx"

    # Load the datasets (adjust based on how your data is structured)
    pn_data = utils.read_data(pn_path, sheet="2020-2023")
    svi_data = utils.read_data(svi_path)
    mmg_data = utils.read_data(mmg_path, sheet='County')
    pop_data = get_population(pop_data_path)

    # Extract county names from each dataset
    svi_counties = svi_data['COUNTY'].dropna().unique().tolist()  # Replace with actual column name for counties in SVI dataset
    pn_counties = pn_data['SourceCounty'].dropna().unique().tolist()    # Replace with actual column name for counties in PulseNet dataset
    mmg_counties = mmg_data['County, State'].dropna().unique().tolist()  # Replace with actual column name for counties in MMG dataset
    pop_counties = pop_data['County'].unique().tolist()  # Assuming pop_data is already loaded as shown in your initial code

    # Initialize empty lists to store matched counties
    matched_svi = []
    matched_pn = []
    matched_mmg = []

    # Perform fuzzy matching for each county in svi, pn, and mmg with pop_data counties
    for county in tqdm(pop_counties):
        matched_svi.append(match_counties(county, svi_counties))
        matched_pn.append(match_counties(county, pn_counties))
        matched_mmg.append(match_counties(county, mmg_counties))

    # Find the maximum length to pad lists accordingly
    max_length = max(len(svi_counties), len(pn_counties), len(mmg_counties))

    # Pad the lists to ensure they are of the same length
    pop_counties = pad_list(pop_counties, max_length)
    svi_counties = pad_list(svi_counties, max_length)
    matched_svi = pad_list(matched_svi, max_length)
    pn_counties = pad_list(pn_counties, max_length)
    matched_pn = pad_list(matched_pn, max_length)
    mmg_counties = pad_list(mmg_counties, max_length)
    matched_mmg = pad_list(matched_mmg, max_length)

    # Create a DataFrame to hold the matched counties
    county_df = pd.DataFrame({
        'Census': pop_counties,
        'Matched SVI County': matched_svi,
        'Matched PulseNet County': matched_pn,
        'Matched MMG County': matched_mmg
    })

    county_df.to_csv(f"{processed_data_path}/matched_counties.csv")
