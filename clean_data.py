'''Code to clean data and save it as a csv.'''

import pandas as pd
import numpy as np
from db_to_pandas import mongo_to_pandas
from pymongo import MongoClient
from requests import get
from unidecode import unidecode
import os


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
    hike_df['gps_coordinates'].iloc[149] = '40 04.674 105 35.077'
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
    h_df = clean_data(df)
    google_api = os.environ['DISTANCE_MATRIX_API']
    hike_df = get_coordinates(h_df, google_api)
    hike_df.to_csv('colorado_hikes.csv')
