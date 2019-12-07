import json
from numpy import NaN
import pandas as pd


def seeburg_to_json():
    # Set general variables
    excel_infile = 'JB-tracking 30nov2019.xlsx'
    singles_sheet = 'SinglesDB'
    layout_sheet = 'Layout'
    json_outfile = 'seeburg.json'


    # Load in the dataframe
    xls = pd.ExcelFile(excel_infile)
    df1 = pd.read_excel(xls, singles_sheet)
    df2 = pd.read_excel(xls, layout_sheet)
    
    # Filter out entries that are not inside the jukebox
    df1 = df1[df1.JB_New.notnull()]
    
    # Drop unnecessary columns
    drop_columns = ['Unnamed: 0', 'Refnr', 'Artist', 'Date Added',
                    'Year_Discogs', 'Sleeve', 'JB_old', 'Unnamed: 9',
                    'Top2000', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16',
                    'Unnamed: 17']
    df1.drop(drop_columns, axis=1, inplace=True)
    df1.rename(columns={'A-side ':'A', 'B-side':'B'}, inplace=True)
    
    # Handle the reverses
    df1 = df1.apply(swap, 1, result_type='broadcast')
    df1.drop('B-side single', axis=1, inplace=True)
    
    # Change index to plate locations
    df1.reset_index(drop=True, inplace=True)
    df1.set_index('JB_New', inplace=True)
    
    # MAKE JSON USING DF2
    
    df2.set_index('index', inplace=True)
    rows, cols = df2.shape
    
    datastore = {}
    for colnr in range(1,int(cols/2)+1):
    
        datastore_column = {}
        for rownr in range(1,int(rows/2)+1):
        
            pos_tl = df2.loc[rownr, colnr]
            pos_bl = df2.loc[f'{rownr}b', colnr]
            pos_tr = df2.loc[rownr, f'{colnr}b']
            pos_br = df2.loc[f'{rownr}b', f'{colnr}b']
            
            svg_set = get_set(pos_tl, pos_bl, pos_tr, pos_br, df1)
            
            datastore_column[rownr] = svg_set
            
        datastore[colnr] = datastore_column
    
    json.dump(datastore, open(json_outfile, 'w'), indent=4, sort_keys=True)
    

def swap(x):
    if x['B-side single'] == 1:
        return [x[1], x[0], x[2], x[3], 0, x[5]]
    else:
        return [x[0], x[1], x[2], x[3], 0, x[5]]


def get_set(pos_tl, pos_bl, pos_tr, pos_br, df):
    datastore = {'left': {'A': {}, 'B': {}}, 'right': {'A': {}, 'B': {}}}
    
    for labelside in datastore.keys():
        pos = pos_tr if labelside == 'right' else pos_tl
        row = df.loc[pos]
        
        datastore[labelside]['artist'] = row[3]
        datastore[labelside]['year'] = row[2]
        
        for plateside in datastore[labelside].keys():
            if plateside == 'A':
                datastore[labelside][plateside]['position'] = pos
                datastore[labelside][plateside]['track'] = row[0]
            elif plateside == 'B':
                pos = pos_br if labelside == 'right' else pos_bl
                datastore[labelside][plateside]['position'] = pos
                datastore[labelside][plateside]['track'] = row[1]
                
    return datastore

if __name__ == '__main__':
    seeburg_to_json()
    pass