import pandas as pd
import numpy as np

def create_features(df):
    df['waterfall'] = 0
    df['lake'] = 0
    df['river'] = 0
    df['summit'] = 0
    df['family_friendly'] = 0
    df['wildlife'] = 0
    df['wildflowers'] = 0
    df['fall_foliage'] = 0
    df['campsite'] = 0
    df['crowded'] = 0
    return df

def add_feature_values(df):
    for idx, desc in enumerate(df['lemmatized_text']):
        if ('waterfall' in desc):
            df['waterfall'].iloc[idx] = 1
        if ('lake' in desc):
            df['lake'].iloc[idx] = 1
        if ('river' in desc):
            df['river'].iloc[idx] = 1
        if ('summit' in desc):
            df['summit'].iloc[idx] = 1
        if ('family' in desc) or ('children' in desc):
            df['family_friendly'].iloc[idx] = 1
        if ('wildlife' in desc):
            df['wildlife'].iloc[idx] = 1
        if ('wildflower' in desc):
            df['wildflowers'].iloc[idx] = 1
        if ('fall' in desc) or ('autumn' in desc):
            df['fall_foliage'].iloc[idx] = 1
        if ('campground' in desc) or ('campsite' in desc):
            df['campsite'].iloc[idx] = 1
        if ('crowd' in desc):
            df['crowded'].iloc[idx] = 1
    for idx, name in enumerate(df['hike_name']):
        if 'Lake' in name:
            df['lake'].iloc[idx] = 1
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/lemmatized_hikes.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)

    df_features = create_features(df)
    new_df = add_feature_values(df_features)

    new_df['dogs_allowed'] = new_df['dogs_allowed'].astype(int)
    new_df['hike_id'] = np.nan
    for idx, name in enumerate(new_df['hike_name']):
        new_df['hike_id'].iloc[idx] = idx
    new_df['hike_id'] = new_df['hike_id'].astype(int)
    new_df.drop('trail_description', axis=1, inplace=True)
    new_df.drop('lemmatized_text', axis=1, inplace=True)

    new_df.to_csv('data/final.csv', index=False)
