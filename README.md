# Introduction

# Project structure

# Scripts

# Data

## Data model creation

To create the data model, run the script `data_model_creation.py`. The following describes how the data model is created.

We used the county level PulseNet data, SVI data, MMG data and census data to create a data model. Since PulseNet data does not contain FIPS codes for counties, we used names of counties as the linkage variable between the PulseNet data and the other datasets. The names of the counties were all changed to match the names in the census data (There are some nuances behind this. Read here for more details & take a look at the code [lines x-x]). The principle of the data model is that the dataset will contain salmonella cases occuring in a state and since a county is a the smallest geographical unit, every row corresponds to the socio-economic conditions (SVI+MMG) and the salmonella rate of a county. As for the period over which the data is relevant, we use data for a single year. Thus, running the script will create a dataset that contains the SVI, MMG, and salmonella rate for each county in the specified state and specified year.

Note: If you run `normalized_county_names.py`, some of the counties of PulseNet won't match those of the other datasets. This is because for some counties, there were no reports of salmonella.

### Edge cases:

A few edge cases were encountered when merging the datasets and they were handled as required. For example, when creating the datamodel for data from Missouri, 2020, an issue was encountered for 'St. Louis city'. PulseNet has separate columns for indicating counties and cities ('SourceCounty' and 'SourceCity'). Thus, 'St. Louis city' didn't exist in the 'SourceCounty' column, which was used as the linkage variable between the PulseNet data and the other datasets. So after we merged, the data model didn't have salmonella data for St. Louis city but did have population, SVI and MMG data. To handle this, we used the following algorithm:

```
for county in state_population_data['County']:
    if county.contains('city'):
        city = fuzz.process.extractOne(county, state_level_pulsenet['SourceCity'].unique())[0]
        city_salmonella_count = state_level_pulsenet[state_level_pulsenet['SourceCity'] == city]['Serotype_wgs'].count()
        # Code to calculate salmonella rate per 100000
        # Code to find SVI and MMG data for the city
        # Code to merge SVI, MMG and salmonella data for the city
```


## Notes about Data collection

# Results

# Discussion