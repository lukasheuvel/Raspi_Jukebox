import json
from numpy import NaN
import pandas as pd


def seeburg_to_json():
    # Set general variables
    excel_infile = 'JB-tracking 30nov2019.xlsx'
    excel_sheet = 'SinglesDB'
    json_outfile = 'seeburg.json'


    # Load in the dataframe
    xls = pd.ExcelFile(excel_infile)
    df1 = pd.read_excel(xls, excel_sheet)
    
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
    
    
    # Set variables for creating json
    labelorder = ['A', 'C', 'E', 'G', 'J']
    number_till = 8
    
    datastore = {}
    for plate_nr in range(number_till):
        plate_nr += 1
        for plate_letter in labelorder:
            svg_set = get_set(plate_letter, str(plate_nr), df1)        
            datastore['set_{}{}'.format(plate_letter, plate_nr)] = svg_set
            
    json.dump(datastore, open(json_outfile, 'w'), indent=4, sort_keys=True)
            
            
def swap(x):
    if x['B-side single'] == 1:
        return [x[1], x[0], x[2], x[3], 0, x[5]]
    else:
        return [x[0], x[1], x[2], x[3], 0, x[5]]


def get_set(l, n, df):
    datastore = {'left': {'A': {}, 'B': {}}, 'right': {'A': {}, 'B': {}}}
    
    for labelside in datastore.keys():
        pos = other_side(l + n, 'label') if labelside == 'right' else l + n
        row = df.loc[pos]
        
        datastore[labelside]['artist'] = row[3]
        datastore[labelside]['year'] = row[2]
        
        for plateside in datastore[labelside].keys():
            if plateside == 'A':
                datastore[labelside][plateside]['position'] = pos
                datastore[labelside][plateside]['track'] = row[0]
            elif plateside == 'B':
                pos = other_side(pos, 'plate')
                datastore[labelside][plateside]['position'] = pos
                datastore[labelside][plateside]['track'] = row[1]
    return datastore
    
def other_side(pos, type):
    if type == 'plate':
        side_dict = {'A':'B', 'C':'D', 'E':'F', 'G':'H', 'J':'K', 'L':'M', 'N':'P',
                  'Q':'R', 'S':'T', 'U':'V', 'B':'A', 'D':'C', 'F':'E', 'H':'G',
                  'K':'J', 'M':'L', 'P':'N', 'R':'Q', 'T':'S', 'V':'U'}
    elif type == 'label':
        side_dict = {'A':'L', 'B':'M', 'C':'N', 'D':'P', 'E':'Q', 'F':'R',
                      'G':'S', 'H':'T', 'J':'U', 'K':'V'}
    pos = side_dict[pos[0]] + pos[1]
    return pos

if __name__ == '__main__':
    seeburg_to_json()
    pass