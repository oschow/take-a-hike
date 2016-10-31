'''Code to turn my mongo database into a pandas dataframe.'''

import pandas as pd
from pymongo import MongoClient

def empty_df():
    '''
    Function to create an empty pandas DataFrame object (used in mongo_to_pandas)
    INPUT: None
    OUTPUT: empty pandas DataFrame object with column titles
    '''
    df = pd.DataFrame(columns=['hike_name',
                               'area_of_co',
                               'round_trip_length',
                               'start_elevation',
                               'end_elevation',
                               'net_elevation_gain',
                               'skill_level',
                               'dogs_allowed',
                               'gps_coordinates',
                               'trail_description'])
    return df


def parse_record(hike):
    row = pd.Series({'hike_name': hike.get('hike_name', None),
                     'area_of_co': hike.get('area_of_co', None),
                     'round_trip_length': hike.get('round_trip_length', None),
                     'start_elevation': hike.get('start_elevation', None),
                     'end_elevation': hike.get('end_elevation', None),
                     'net_elevation_gain': hike.get('net_elevation_gain', None),
                     'skill_level': hike.get('skill_level', None),
                     'dogs_allowed': hike.get('dogs_allowed', None),
                     'gps_coordinates': hike.get('gps_coordinates', None),
                     'trail_description': hike.get('description', None)})
    return row

def mongo_to_pandas(db_table):
    '''
    Function to pull key information from a mongo table into a pandas DataFrame
    INPUT: pymongo collection object
    OUTPUT: pandas DataFrame object
    '''
    df = empty_df()
    df_2 = empty_df()
    c = db_table.find()
    lst = list(c)
    i = 0
    for hike in lst:
        i += 1
        if i % 319 == 0:
            df = df.append(df_2)
            df_2 = empty_df()
        print 'Row {} of {}'.format(i, len(lst))
        row = parse_record(hike)
        df_2 = df_2.append(row, ignore_index=True)
    df = df.append(df_2)
    return df

if __name__ == '__main__':
    client = MongoClient()
    db = client['db_hikes']
    table = db['hikes_table']

    hike_df = mongo_to_pandas(table)
