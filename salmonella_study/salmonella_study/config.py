import os

class Config:
    # Project root directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

    # Specific data directories
    MMG_DATA_DIR = os.path.join(RAW_DATA_DIR, 'mmg')
    PN_DATA_DIR = os.path.join(RAW_DATA_DIR, 'pulsenet')
    SVI_DATA_DIR = os.path.join(RAW_DATA_DIR, 'social_vulnerability_index')
    RAW_POULTRY_DATA_DIR = os.path.join(RAW_DATA_DIR, 'raw_poultry')
    CENSUS_DATA_DIR = os.path.join(RAW_DATA_DIR, 'census')
    NORS_DATA_DIR = os.path.join(RAW_DATA_DIR, 'nors')
    FOODNET_DATA_DIR = os.path.join(RAW_DATA_DIR, 'foodnet')

    # Output directories
    RESULTS_DIR = os.path.join(BASE_DIR, 'results')
    FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
    REPORTS_DIR = os.path.join(RESULTS_DIR, 'reports')

