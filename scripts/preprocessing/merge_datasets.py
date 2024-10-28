# DEFINITION: This script merges the pulsenet, map the meal gap and svi dataset

import pandas as pd
import os
from thefuzz import process, fuzz
from salmonella_study import utils
from salmonella_study import data_processing as processing
from salmonella_study.config import Config
import logging

pd.options.display.max_rows = 300

# paths
raw_data_path = Config.RAW_DATA_DIR
processed_data_path = Config.PROCESSED_DATA_DIR
results_path = Config.RESULTS_DIR

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(svi_path, pn_path, mmg_path, pop_data_path, year, state, state_long):
    logging.info("Reading data...")
    try:
        svi_data = utils.read_data(svi_path)
        pn_data = utils.read_data(pn_path, sheet="2020-2023")
        mmg_data = utils.read_data(mmg_path, sheet='County')
        population_data = processing.get_population(pop_data_path, state_long, year)
    except Exception as e:
        logging.error(f"Error reading data: {e}")
        return

    logging.info("Done reading data. Processing will begin shortly...")

    # convert 'IsolatDate' column into datetime type.
    pn_data["IsolatDate"] = pd.to_datetime(pn_data["IsolatDate"], errors="coerce", format="%m/%d/%y")

    # Replace 'unknown'/'UNKNOWN' counties with NaN's
    pn_data['SourceCounty'] = pn_data['SourceCounty'].replace(['unknown', 'UNKNOWN', ''], pd.NA)

    # select data for specified year and state
    pn_data = pn_data.loc[(pn_data["IsolatDate"].dt.year == year) & (pn_data["SourceState"] == state)].reset_index(drop=True)
    svi_data = svi_data.loc[svi_data["ST_ABBR"] == state].reset_index(drop=True)
    mmg_data = mmg_data.loc[mmg_data['State'] == state].reset_index(drop=True)

    # Replace County names in PulseNet with County names in population data
    county_names = population_data['County'].unique()
    pn_data['County normalized'] = pn_data['SourceCounty'].apply(lambda x: process.extractOne(x, county_names, scorer=fuzz.token_sort_ratio)[0] if pd.notna(x) else pd.NA)

    # Calculate salmonella rate per County
    salmonella_per_county_df = pn_data.groupby(["County normalized", "SourceState"])["Serotype_wgs"].count().reset_index(name="salmonella_count").rename(columns={"County normalized": "County"})
    salmonella_per_county_df.sort_values(by='County', inplace=True)
    salmonella_per_county_df.rename(columns={"SourceState": "State"}, inplace=True)

    # Calculate salmonella rate per city
    # salmonella_per_city_df = pn_data.groupby('SourceCity')['Serotype_wgs'].count().reset_index(name='salmonella_count').rename(columns={'SourceCity': 'City'})

    # Merge salmonella and population data
    salmonella_per_county_df = pd.merge(salmonella_per_county_df, population_data, how="outer", on="County").reset_index(drop=True)
    salmonella_per_county_df.rename(columns={year: f"{year} population"}, inplace=True)

    # Fill NaN values in SourceState with State abbreviation
    salmonella_per_county_df['State'] = salmonella_per_county_df['State'].fillna(state)

    # Calculate salmonella rate (salmonella cases per 100,000 persons).
    salmonella_per_county_df['salmonella per 100000'] = (salmonella_per_county_df["salmonella_count"]/salmonella_per_county_df[f'{year} population']) * 100000

    # Save salmonella per county data
    save_path = os.path.join(processed_data_path, "salmonella_population", f"salmonella_per_county_{state}_{year}.csv")
    salmonella_per_county_df.to_csv(save_path, index=False)
    logging.info(f"Saved salmonella per county data to {save_path}")

    # Prepare SVI for merging
    svi_data.rename(columns={'COUNTY': 'County'}, inplace=True)
    svi_data["County normalized"] = svi_data["County"].apply(lambda x: process.extractOne(x, county_names, scorer=fuzz.token_sort_ratio)[0])
    svi_data = svi_data.drop(columns=(col for col in svi_data.columns if col.startswith('M')))
    svi_data = svi_data.drop(columns=['ST', 'STATE', 'ST_ABBR'])

    # merge svi and salmonella per County
    merged = pd.merge(svi_data, salmonella_per_county_df, how="outer", on="County")
    save_path = os.path.join(processed_data_path, "salmonella_population", f"svi_vs_salmonella-rate_{state}_{year}.csv")
    merged.to_csv(save_path, index=False)

    logging.info("SVI and salmonella rates have been merged. Look into the \
                 file and check for edge cases and deal with them manually \
                 before continuing the merging process.")
    user_confirmation = input("\nHave you dealt with edge cases? (y/n): ")

    # Exit function if user has not handled edge cases
    while True:
        user_confirmation = input("\nHave you dealt with edge cases? (y/n): ").lower()
        if user_confirmation == 'y':
            break
        elif user_confirmation == 'n':
            logging.info("Please handle the edge cases before continuing. Check the saved file at: " + save_path)
        else:
            logging.info("Invalid input. Please enter 'y' or 'n'")
    
    # This merged df was modified manually in csv form to make it look nicer
    # Load the csv instead of using the 'merged' df
    merged = pd.read_csv(save_path)

    # Prepare MMG for merging
    mmg_data.rename(columns={'County, State': 'County'}, inplace=True)
    mmg_data['County'] = mmg_data['County'].apply(lambda x: process.extractOne(x, county_names, scorer=fuzz.token_sort_ratio)[0])

    # Merge
    merged = pd.merge(merged, mmg_data, how='outer', on='County')

    # Reposition columns so that salmonella rate and salmonella per 100000 are at the end
    cols = merged.columns.tolist()
    salmonella_cols = [col for col in cols if 'salmonella' in col.lower()]
    cols.pop(cols.index('salmonella_count'))
    cols.pop(cols.index('salmonella per 100000'))
    cols.extend(salmonella_cols)
    merged = merged[cols]

    # Save merged data
    save_path = os.path.join(processed_data_path, "salmonella_population", f"sense-d_socioecono_salmonella_{state}_{year}.csv")
    merged.to_csv(save_path, index=False)
    logging.info(f"Saved merged data to {save_path}")

    # Uncomment the following block if correlation analysis is needed
    """
    # correlation matrix
    merged_numeric = merged.select_dtypes(include=["number"])
    corr = merged_numeric.corr()

    # save correlation result
    corr_save_path = os.path.join(results_path, "correlation_results", f"{state}_{year}_corr.csv")
    corr.to_csv(corr_save_path, float_format='%.5f')
    logging.info(f"Saved correlation matrix to {corr_save_path}")

    # sort correlations
    salmonella_correlations = corr['salmonella per 100000'].sort_values(ascending=False)
    logging.info("Top 10 and Bottom 10 correlations:")
    logging.info(salmonella_correlations.head(10))
    logging.info(salmonella_correlations.tail(10))

    # save correlations
    corr_save_path = os.path.join(results_path, "correlation_results", f"salmonella_correlations_{state}_{year}.csv")
    salmonella_correlations.to_csv(corr_save_path, float_format='%.5f')
    logging.info(f"Saved salmonella correlations to {corr_save_path}")
    """

if __name__ == "__main__":
    # Specify year and state
    year = 2020 
    state = 'MO'
    state_long = 'Missouri' 

    svi_path = os.path.join(Config.SVI_DATA_DIR, f"SVI_{year}_US_county.csv")
    pn_path = os.path.join(Config.PN_DATA_DIR, "Export_2020-2023.xlsx")
    mmg_path = os.path.join(Config.MMG_DATA_DIR, "MMG2022_2020-2019Data_ToShare.xlsx")
    pop_data_path = os.path.join(Config.CENSUS_DATA_DIR, "2020-2023.xlsx")
    
    # Double-check if user has picked the correct paths to the data
    logging.info("Running script for the following data specs")
    logging.info(f"SVI: {svi_path}")
    logging.info(f"PulseNet: {pn_path}")
    logging.info(f"Map the Meal Gap: {mmg_path}")
    logging.info(f"Population: {pop_data_path}")
    logging.info(f"Year: {year}")
    logging.info(f"State: {state}")

    user_confirmation = input("\nProceed? (y/n): ")
    if user_confirmation.lower() == 'y':
        main(svi_path, pn_path, mmg_path, pop_data_path, year, state, state_long) 
        logging.info("Processing complete!")
    else:
        logging.info("Script execution cancelled by user.")
