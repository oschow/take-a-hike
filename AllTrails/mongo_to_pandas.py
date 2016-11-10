'''Code to turn my mongo database of AllTrails data into a pandas dataframe.'''

import pandas as pd
from pymongo import MongoClient

client = MongoClient()
db = client['rating_db']
table = db['hikes']

def empty_df():
    '''
    Function to create an empty pandas DataFrame object (used in mongo_to_pandas)
    INPUT: None
    OUTPUT: empty pandas DataFrame object with column titles
    '''
    df = pd.DataFrame(columns=['hike_name',
                               'hike_region',
                               'total_distance',
                               'elevation_gain',
                               'hike_difficulty',
                               'route_type',
                               'hike_attributes',
                               'num_reviews',
                               'stars',
                               'ratings'])
    return df


def parse_record(hike):
    row = pd.Series({'hike_name': hike.get('hike_name', None),
                     'hike_region': hike.get('hike_region', None),
                     'total_distance': hike.get('total_distance', None),
                     'elevation_gain': hike.get('elevation_gain', None),
                     'hike_difficulty': hike.get('hike_difficulty', None),
                     'route_type': hike.get('route_type', None),
                     'hike_attributes': hike.get('hike_attributes', None),
                     'num_reviews': hike.get('num_reviews', None),
                     'stars': hike.get('stars', None),
                     'ratings': hike.get('ratings', None)})
    return row

def turn_into_pandas(db_table):
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
        row = parse_record(hike)
        df_2 = df_2.append(row, ignore_index=True)
    df = df.append(df_2)
    return df

hike_df = turn_into_pandas(table)

if __name__ == '__main__':
    pass
