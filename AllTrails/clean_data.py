'''Code to clean AllTrails data and save it as a csv.'''

import pandas as pd
import numpy as np
from mongo_to_pandas import turn_into_pandas
from pymongo import MongoClient
from collections import defaultdict
import cPickle as pickle

def create_user_hike_rating_dict(hike_df, user_ids):
    user_hike_rating_dict = defaultdict(dict)
    for idx, lst in enumerate(hike_df['ratings']):
        for user_dict in lst:
            for user, rating in user_dict.iteritems():
                user_id = user_ids[user]
                hike_id = hike_df['hike_id'].iloc[idx]
                user_hike_rating_dict[user_id][hike_id] = rating
    return user_hike_rating_dict

def create_user_ids(hike_df):
    users = []
    for idx, lst in enumerate(hike_df['ratings']):
        for user_dict in lst:
            for user, rating in user_dict.iteritems():
                users.append(user)
    set_of_users = set(users)
    user_ids = {}
    num = 1
    for unique_user in set_of_users:
        user_ids[unique_user] = 'user{}'.format(num)
        num += 1
    return user_ids

def create_hike_ids(df):
    df['hike_id'] = 0
    for idx, name in enumerate(df['hike_name']):
        df['hike_id'].iloc[idx] = 'hike{}'.format(idx)
    hike_ids = {}
    for idx, _id in enumerate(df['hike_id']):
        hike_ids[_id] = df['hike_name'].iloc[idx]
    return df, hike_ids

def add_features(hike_df):
    hike_df['dog_friendly'] = 0
    hike_df['kid_friendly'] = 0
    hike_df['camping'] = 0
    hike_df['waterfall'] = 0
    hike_df['river'] = 0
    hike_df['lake'] = 0
    hike_df['wildflowers'] = 0
    hike_df['wildlife'] = 0
    hike_df['views'] = 0
    for idx, attributes in enumerate(hike_df['hike_attributes']):
        for feature in attributes:
            if feature == 'dog friendly' or feature == 'dogs on leash':
                hike_df['dog_friendly'].iloc[idx] = 1
            if feature == 'kid friendly':
                hike_df['kid_friendly'].iloc[idx] = 1
            if feature == 'camping':
                hike_df['camping'].iloc[idx] = 1
            if feature == 'waterfall':
                hike_df['waterfall'].iloc[idx] = 1
            if feature == 'river':
                hike_df['river'].iloc[idx] = 1
            if feature == 'lake':
                hike_df['lake'].iloc[idx] = 1
            if feature == 'wild flowers':
                hike_df['wildflowers'].iloc[idx] = 1
            if feature == 'wildlife':
                hike_df['wildlife'].iloc[idx] = 1
            if feature == 'views':
                hike_df['views'].iloc[idx] = 1
    hike_df.drop('hike_attributes', axis=1, inplace=True)
    return hike_df

def add_route_type(hike_df):
    hike_df['loop'] = 0
    hike_df['out_and_back'] = 0
    hike_df['point_to_point'] = 0
    for idx, hike_type in enumerate(hike_df['route_type']):
        if hike_type == 'Loop':
            hike_df['loop'].iloc[idx] = 1
        if hike_type == 'Out & Back':
            hike_df['out_and_back'].iloc[idx] = 1
        if hike_type == 'Point to Point':
            hike_df['point_to_point'].iloc[idx] = 1
    hike_df.drop('route_type', axis=1, inplace=True)
    return hike_df

def clean_data(hike_df):
    hike_df['elevation_gain'] = hike_df['elevation_gain'].str.replace(' feet','')
    hike_df['elevation_gain'] = hike_df['elevation_gain'].astype(int)
    hike_df['total_distance'] = hike_df['total_distance'].str.replace(' miles','')
    hike_df['total_distance'] = hike_df['total_distance'].astype(float)
    hike_df['stars'] = hike_df['stars'].astype(float)
    hike_df['hike_difficulty'] = hike_df['hike_difficulty'].map({'EASY': 1, 'MODERATE': 2, 'HARD': 3})
    hike_df = add_route_type(hike_df)
    hike_df = add_features(hike_df)
    return hike_df


if __name__ == '__main__':
    client = MongoClient()
    db = client['rating_db']
    table = db['hikes']

    df = turn_into_pandas(table)
    df = df.dropna()
    df.drop('num_reviews', axis=1, inplace=True)
    df = df[df['hike_difficulty'] != 'DIFFICULTY']
    h_df, hike_ids = create_hike_ids(df)
    hike_df = clean_data(h_df)
    user_ids = create_user_ids(hike_df)
    user_hike_rating_dict = create_user_hike_rating_dict(hike_df, user_ids)
    hike_df.drop('ratings', axis=1, inplace=True)
    hike_df.to_csv('data/all_hikes_with_hike_name.csv', index=False)
    hike_df.drop('hike_name', axis=1, inplace=True)
    hike_df.to_csv('data/all_hikes_with_hike_id.csv', index=False)

    rating_df = pd.DataFrame.from_dict(user_hike_rating_dict)
    rating_df['hike_id'] = rating_df.index
    hike_user_rating_df = pd.melt(rating_df, id_vars='hike_id').dropna()
    hike_user_rating_df.to_csv('data/all_ratings_matrix.csv', index=False)

    with open('data/all_hike_ids.pkl', 'w') as f:
        pickle.dump(hike_ids, f)
    with open('data/all_user_ids.pkl', 'w') as f:
        pickle.dump(user_ids, f)
