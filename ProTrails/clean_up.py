import pandas as pd
import numpy as np

def clean_hike_names(df):
    df['hike_name'].iloc[37] = 'Sunnyside - Shadyside Loop'
    df['hike_name'].iloc[50] = 'Eagle - Sage Lollipop Loop'
    df['hike_name'].iloc[52] = 'Sleepy Lion Trail - Button Rock Dam Loop'
    df['hike_name'].iloc[60] = 'McClintock - Enchanted Mesa Loop'
    df['hike_name'].iloc[63] = 'Doudy Draw - Spring Brook Loop Trail'
    df['hike_name'].iloc[65] = 'Eldorado Canyon - Walker Ranch Lollipop Loop'
    df['hike_name'].iloc[67] = 'Fowler Trail - Self Guided Nature Walk'
    df['hike_name'].iloc[72] = 'Goshawk Ridge Trail - Spring Brook North Loop'
    df['hike_name'].iloc[78] = 'Ute Trail - Range View Trail Loop'
    df['hike_name'].iloc[86] = 'Green Mountain - Bear Peak Trail (Green and Bear It)'
    df['hike_name'].iloc[87] = 'Greyrock Trail - Greyrock Meadows Loop Trail'
    df['hike_name'].iloc[101] = 'Marshall Valley - Cowdrey Draw Trail'
    df['hike_name'].iloc[106] = 'North Table - Tilting Mesa - Mesa Top Loop'
    df['hike_name'].iloc[113] = 'Mesa Trail - Big Bluestem Trail Loop'
    df['hike_name'].iloc[116] = 'Teller Farms - East Boulder Trail'
    df['hike_name'].iloc[119] = 'Belcher Hill - Rawhide - Longhorn - Whippletree Loop'
    df['hike_name'].iloc[142] = 'Long Lake - Jean Lunning Loop Trail'
    df['hike_name'].iloc[166] = 'King Lake - High Lonesome - Devils Thumb Lake Loop'
    df['hike_name'].iloc[182] = '5 Lake Loop: Bear-Helene-Odessa-Fern-Cub'
    df['hike_name'].iloc[272] = 'Fredonia Gulch to Hoosier Ridge - Red Mountain'
    df['hike_name'].iloc[303] = 'Missouri Pass - Fancy Pass Loop'
    df['hike_name'] = df['hike_name'].str.strip()
    return df

def fix_duplicate_names(df):
    df['hike_name'].iloc[33] = 'Blue Lake (Aspen-Snowmass)'
    df['hike_name'].iloc[139] = 'Blue Lake (Indian Peaks Wilderness Area)'
    df['hike_name'].iloc[212] = 'Blue Lake (Rocky Mountain National Park)'
    df['hike_name'].iloc[59] = 'Mallory Cave (Boulder - Chautauqua Park Trailhead)'
    df['hike_name'].iloc[104] = 'Mallory Cave (Boulder - NCAR Mesa Trailhead)'
    df['hike_name'].iloc[186] = 'Lake Haiyaha (RMNP - Bear Lake Trailhead)'
    df['hike_name'].iloc[216] = 'Lake Haiyaha (RMNP - Glacier Gorge Trailhead)'
    df['hike_name'].iloc[173] = 'Cascade Falls (Indian Peaks Wilderness Area)'
    df['hike_name'].iloc[234] = 'Cascade Falls (Rocky Mountain National Park)'
    df['hike_name'].iloc[195] = 'Mirror Lake (Rocky Mountain National Park)'
    df['hike_name'].iloc[292] = 'Mirror Lake (Summit County - Eagles Nest Wilderness Area)'
    df['hike_name'].iloc[224] = 'Crystal Lakes (Rocky Mountain National Park)'
    df['hike_name'].iloc[313] = 'Crystal Lakes (Summit County - Eagle County - Clear Creek County)'
    return df

def fix_data_type(df):
    df['dogs_allowed'] = df['dogs_allowed'].map({'Yes': 1, 'No': 0}).astype(bool)
    df3['drive_time_from_denver'] = df3['drive_time_from_denver'].astype(float)
    df['skill_level'] = df['skill_level'].map({'Easy': 1, 'Easy-Moderate': 2, 'Moderate': 3, 'Moderate-Strenuous': 4, 'Strenuous': 5})
    return df

def drop_unnecessary_columns(df):
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('latitude', axis=1, inplace=True)
    df.drop('longitude', axis=1, inplace=True)
    return df

if __name__ == '__main__':
    df1 = pd.read_csv('data/colorado_hikes.csv')
    df2 = clean_hike_names(df1)
    df3 = fix_duplicate_names(df2)
    df4 = fix_data_type(df3)
    hike_df = drop_unnecessary_columns(df4)

    hike_df.to_csv('data/hike_data_clean.csv')
