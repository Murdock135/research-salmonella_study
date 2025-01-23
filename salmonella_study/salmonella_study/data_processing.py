import pandas as pd

def modify_county_names(county_name: str):
    """Title-ize county names and remove the word 'County'. For example, 'St. Louis County' -> 'St. Louis'
    """

    return county_name.replace("County", "").title().strip()

def get_population(population_xlsx_path, state_long=None, year=None) -> pd.DataFrame:
    # read excel file
    population_xlsx = pd.ExcelFile(population_xlsx_path)
    sheet_name = population_xlsx.sheet_names[0]  # census population xlsx file has only 1 sheet
    population_data = pd.read_excel(population_xlsx, sheet_name=sheet_name, skiprows=3)  # first 3 rows are irrelevant
    population_data = population_data[:-6]  # last 6 rows are irrelevant
    population_data = population_data.drop(columns=population_data.columns[1])  # 2nd column is irrelevant

    # Rename County column
    population_data.rename(columns={population_data.columns[0]: "County"}, inplace=True)

    if state_long is not None:
        # Filter data to get state population
        population_data = population_data.loc[population_data['County'].str.lower().str.contains(state_long.lower())].reset_index(drop=True)

    # Remove the leading '.', ', {state_long}' and 'County' from all rows in 'County' column
    population_data["County"] = population_data["County"].str.lstrip('.')
    population_data["County"] = population_data["County"].str.replace(f", {state_long}", "", regex=False)
    population_data["County"] = population_data["County"].str.replace("County", "", regex=False)
    population_data["County"] = population_data["County"].str.strip()
    population_data["County"] = population_data["County"].str.title()

    if year is not None:
        return population_data[["County", year]]
    else:
        return population_data
    
def rearrange_cols(df, col_positions):
    cols = df.columns.tolist()
    
    for col, pos in col_positions.items():
        cols.remove(col)
        cols.insert(pos, col)

    return df.reindex(columns=cols)


