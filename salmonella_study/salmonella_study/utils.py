import os
import pandas as pd
import matplotlib.pyplot as plt

def read_data(path, **kwargs):
    '''Note: If using excel, provide the sheet name in kwargs'''
    if os.path.exists(path):
        if kwargs:
            data = pd.read_excel(path, sheet_name= kwargs['sheet'])
        else:
            data = pd.read_csv(path)
        return data
    else:
        print(f"path {path} does not exist")
        return None
    
def save_fig(fig, dir, file_name):
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    fig.savefig(os.path.join(dir, file_name), format='png')
