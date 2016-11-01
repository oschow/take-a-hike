'''Code to clean data and save it as a csv.'''

import pandas as pd
import numpy as np
from db_to_pandas import mongo_to_pandas
from pymongo import MongoClient
from requests import get
from unidecode import unidecode
import os

def add_missing_gps_coordinates(hike_df):
    hike_df['gps_coordinates'].iloc[69] = '39 57.597 105 14.234'
    hike_df['gps_coordinates'].iloc[76] = '40 00.102 105 18.450'
    hike_df['gps_coordinates'].iloc[77] = '40 00.102 105 18.450'
    hike_df['gps_coordinates'].iloc[78] = '40 00.102 105 18.450'
    hike_df['gps_coordinates'].iloc[91] = '40 08.964 105 18.005'
    hike_df['gps_coordinates'].iloc[103] = '39 58.656 105 30.582'
    hike_df['gps_coordinates'].iloc[104] = '39 58.698 105 16.500'
    hike_df['gps_coordinates'].iloc[124] = '39 49.133 105 17.194'
    hike_df['gps_coordinates'].iloc[125] = '39 06.054 108 44.088'
    hike_df['gps_coordinates'].iloc[126] = '39 06.050 108 44.100'
    hike_df['gps_coordinates'].iloc[127] = '39 06.050 108 44.100'
    hike_df['gps_coordinates'].iloc[130] = '39 04.663 108 43.687'
    hike_df['gps_coordinates'].iloc[131] = '39 04.663 108 43.687'
    hike_df['gps_coordinates'].iloc[133] = '39 06.050 108 44.100'
    hike_df['gps_coordinates'].iloc[149] = '40 04.674 105 35.077'
    hike_df['gps_coordinates'].iloc[183] = '40 18.716 105 38.761'
    hike_df['gps_coordinates'].iloc[188] = '40 18.716 105 38.761'
    hike_df['gps_coordinates'].iloc[195] = '40 30.983 105 46.188'
    hike_df['gps_coordinates'].iloc[219] = '40 14.412 105 49.614'
    hike_df['gps_coordinates'].iloc[226] = '40 24.439 105 37.564'
    hike_df['gps_coordinates'].iloc[241] = '40 19.200 105 36.283'
    hike_df['gps_coordinates'].iloc[247] = '40 22.372 105 36.845'
    hike_df['gps_coordinates'].iloc[308] = '39 37.869 106 03.986'
    return hike_df

def clean_data(hike_df):
    columns = ['start_elevation', 'end_elevation', 'gps_coordinates', 'trail_description']
    for col in columns:
        hike_df[col] = hike_df[col].apply(unidecode)
    remove_these_1 = [',', "'", '.', '-', '`', '+', '(']
    for char in remove_these_1:
        hike_df['start_elevation'] = hike_df['start_elevation'].str.replace(char,'')
        hike_df['end_elevation'] = hike_df['end_elevation'].str.replace(char,'')
    hike_df['net_elevation_gain'].iloc[164] = '1805'
    hike_df['net_elevation_gain'].iloc[76] = '20'
    hike_df['net_elevation_gain'].iloc[117] = '0'
    hike_df['net_elevation_gain'].iloc[118] = '0'
    hike_df['net_elevation_gain'].iloc[46] = '0'
    hike_df['net_elevation_gain'].iloc[44] = '0'
    remove_these_2 = [',', "'", '.', '`', '+']
    for chars in remove_these_2:
        hike_df['net_elevation_gain'] = hike_df['net_elevation_gain'].str.replace(chars,'')
    hike_df['start_elevation'] = hike_df['start_elevation'].astype(int)
    hike_df['end_elevation'] = hike_df['end_elevation'].astype(int)
    hike_df['net_elevation_gain'] = hike_df['net_elevation_gain'].apply(unidecode)
    hike_df['net_elevation_gain'] = hike_df['net_elevation_gain'].str.replace("'",'')
    hike_df['net_elevation_gain'] = hike_df['net_elevation_gain'].astype(int)
    hike_df['latitude'] = None
    hike_df['longitude'] = None
    for idx, row in enumerate(hike_df['gps_coordinates']):
        r = row.split()
        if r[0] != 'Null':
            r0 = r[0].replace('N', '').strip()
            r2 = r[2].replace('W', '').strip()
            hike_df['latitude'].iloc[idx] = r0 + '.' + str(float(r[1])/60).split('.')[1]
            hike_df['longitude'].iloc[idx] = '-' + r2 + '.' + str(float(r[3])/60).split('.')[1]
    hike_df.drop('gps_coordinates', axis=1, inplace=True)
    hike_df['drive_time_from_denver'] = None
    return hike_df


def get_drive_time(string, google_api):
    """Uses the Google API to calculate drive time from Denver."""
    try:
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Denver&destinations={0}&avoid=toll&key={1}'.format(string, google_api)
        response = get(url)
        if response.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(response.status_code))
        else:
            return response.json()['rows'][0]['elements'][0]['duration']['value']/float(60)
    except:
        return 'Problems'

def get_coordinates(hike_df, google_api):
    for idx, row in enumerate(hike_df['latitude']):
        if row == None:
            hike_df['drive_time_from_denver'].iloc[idx] = np.nan
        else:
            string = hike_df['latitude'].iloc[idx] + ',' + hike_df['longitude'].iloc[idx]
            hike_df['drive_time_from_denver'].iloc[idx] = get_drive_time(string, google_api)
    return hike_df


if __name__ == '__main__':
    client = MongoClient()
    db = client['hike_database']
    table = db['hikes']

    df = mongo_to_pandas(table)
    df1 = add_missing_gps_coordinates(df)
    h_df = clean_data(df1)
    google_api = os.environ['DISTANCE_MATRIX_API']
    hike_df = get_coordinates(h_df, google_api)
    hike_df.to_csv('colorado_hikes.csv')
